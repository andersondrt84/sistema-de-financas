import os
from datetime import datetime
from decimal import Decimal

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "troque-esta-chave")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/financas_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    incomes = db.relationship("Income", backref="user", lazy=True, cascade="all, delete-orphan")
    expenses = db.relationship("Expense", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def to_decimal(value: str) -> Decimal:
    value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return Decimal(value)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Usuário ou senha inválidos.", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.created_at.desc()).all()
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.created_at.desc()).all()

    total_income = sum((i.amount for i in incomes), Decimal("0"))
    total_discount = sum((i.discount for i in incomes), Decimal("0"))
    total_expense = sum((e.amount for e in expenses), Decimal("0"))
    net_income = total_income - total_discount
    balance = net_income - total_expense

    return render_template(
        "dashboard.html",
        incomes=incomes,
        expenses=expenses,
        total_income=total_income,
        total_discount=total_discount,
        total_expense=total_expense,
        net_income=net_income,
        balance=balance,
    )


@app.route("/incomes", methods=["POST"])
@login_required
def add_income():
    try:
        income = Income(
            description=request.form.get("description", "Sem descrição").strip() or "Sem descrição",
            amount=to_decimal(request.form.get("amount", "0")),
            discount=to_decimal(request.form.get("discount", "0")),
            user_id=current_user.id,
        )
        db.session.add(income)
        db.session.commit()
        flash("Entrada adicionada com sucesso.", "success")
    except Exception:
        db.session.rollback()
        flash("Erro ao adicionar entrada. Verifique os valores.", "error")
    return redirect(url_for("dashboard"))


@app.route("/expenses", methods=["POST"])
@login_required
def add_expense():
    try:
        expense = Expense(
            description=request.form.get("description", "Sem descrição").strip() or "Sem descrição",
            amount=to_decimal(request.form.get("amount", "0")),
            user_id=current_user.id,
        )
        db.session.add(expense)
        db.session.commit()
        flash("Despesa adicionada com sucesso.", "success")
    except Exception:
        db.session.rollback()
        flash("Erro ao adicionar despesa. Verifique os valores.", "error")
    return redirect(url_for("dashboard"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        if not current_user.check_password(current_password):
            flash("Senha atual incorreta.", "error")
        elif len(new_password) < 8:
            flash("A nova senha deve ter pelo menos 8 caracteres.", "error")
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash("Senha alterada com sucesso.", "success")
            return redirect(url_for("profile"))

    return render_template("profile.html")


def seed_default_user():
    user = User.query.filter_by(username="anderson").first()
    if not user:
        user = User(username="anderson")
        user.set_password("12345678")
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_default_user()
    app.run(host="0.0.0.0", port=6000, debug=True)
