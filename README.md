# Sistema de Finanças Web

Aplicação Flask com PostgreSQL para controle financeiro pessoal por usuário.

## Recursos
- Login com usuário padrão `anderson` e senha `12345678`.
- Dashboard com cadastro de ganhos, descontos e despesas.
- Cálculo automático do saldo final (positivo/negativo).
- Página de perfil para alterar senha.
- Dados separados por usuário.

## Requisitos
- Python 3.11+
- PostgreSQL

## Configuração
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure a variável de ambiente (exemplo):
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/financas_db"
```

## Execução
```bash
python app.py
```
A aplicação iniciará na porta **6000**.
