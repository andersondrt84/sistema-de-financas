# Sistema de Finanças Web

Aplicação Flask com PostgreSQL para controle financeiro pessoal por usuário.

## Recursos
- Login com usuário padrão `anderson` e senha `12345678`.
- Dashboard com cadastro de ganhos, descontos e despesas.
- Cálculo automático do saldo final (positivo/negativo).
- Página de perfil para alterar senha.
- Dados separados por usuário.
- Pronto para subir com Docker e Portainer (stack).

## Rodando com Docker (recomendado)
```bash
docker compose up -d --build
```

A aplicação ficará em: `http://SEU_HOST:6000`

### Serviços da stack
- `web`: aplicação Flask com Gunicorn (leve para produção).
- `db`: PostgreSQL 16 Alpine com volume persistente.

## Subindo no Portainer (Stack)
1. No Portainer, abra **Stacks** > **Add stack**.
2. Dê um nome para a stack (ex.: `financas`).
3. Cole o conteúdo do arquivo `docker-compose.yml`.
4. Clique em **Deploy the stack**.
5. Acesse `http://SEU_IP:6000`.

## Credenciais iniciais
- Usuário: `anderson`
- Senha: `12345678`

> Troque `SECRET_KEY` e senha do banco antes de produção.

## Execução local sem Docker (opcional)
### Requisitos
- Python 3.11+
- PostgreSQL

### Configuração
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/financas_db"
python app.py
```

A aplicação iniciará na porta **6000**.
