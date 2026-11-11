# Elo · Finanças em família

Aplicação em português para acompanhar receitas do casal, despesas, custos mensais recorrentes, limites mensais e oportunidades de economia. Valores em reais, com cálculos em centavos.

## Executar

Requer Node.js 20 ou superior. Sem dependências externas de execução.

```sh
npm start
```

Servidor na porta 3000 (altere com `PORT`). Para validar os cálculos: `npm test`.

## Uso

Adicione receitas e despesas, selecione o responsável e marque despesas ou receitas recorrentes. A recorrência aparece a partir do mês inicial; editar ou excluir afeta toda a série. Defina uma meta de despesas para cada mês. O botão “Explorar exemplo” permite conhecer a aplicação e remover os dados demonstrativos depois.

Os dados são armazenados no localStorage deste navegador, sem conta, servidor de dados ou sincronização entre dispositivos. Não há integração bancária. Use Exportar backup regularmente: limpar os dados do navegador pode apagar os registros. Importar backup substitui os registros atuais após confirmação. As sugestões de redução são simulações simples.

## Estrutura

- `src/finance.js`: seleção mensal, recorrências e cálculos.
- `src/app.js`: interface, armazenamento e backup.
- `src/style.css`: layout responsivo.
- `server.js`: servidor estático local.

## Docker e Portainer (Docker Standalone)

No Portainer, selecione o ambiente Docker e abra **Stacks → Add stack → Repository**:

- Nome: `elo-financas`
- Repository URL: `https://github.com/andersondrt84/sistema-de-financas`
- Repository reference: `refs/heads/main`
- Compose path: `compose.yaml`
- Se o repositório for privado, configure a autenticação Git no próprio Portainer, com acesso de leitura. Não inclua tokens nos arquivos.
- Opcional: variável `APP_PORT` para escolher uma porta livre (padrão `3080`).

Clique em **Deploy the stack**. O Portainer precisa conseguir clonar o repositório, construir a imagem e baixar `node:24-alpine` do Docker Hub. Aguarde o container ficar `healthy`. Acesse `http://IP_DO_SERVIDOR:3080` (ou a porta configurada). Use HTTPS no proxy reverso para acesso pela Internet.

Se sua versão/edição do Portainer não conseguir construir com o contexto do repositório, clone o projeto no host Docker e execute:

```sh
git clone https://github.com/andersondrt84/sistema-de-financas.git
cd sistema-de-financas
docker compose up -d --build
docker compose ps
```

O container também aparecerá no Portainer. Para atualizar, use `git pull --ff-only` e `docker compose up -d --build` nessa pasta. No painel, use a atualização da stack via Git com reconstrução da imagem quando disponível.

### Persistência e acesso do casal

Esta versão guarda os lançamentos no navegador (localStorage), não no container. Reiniciar o container não apaga esses dados; limpar o navegador apaga. Não existe banco de dados, login ou sincronização entre você e sua esposa. Cada navegador tem seus próprios registros. Exporte o backup antes de mudar endereço, porta ou protocolo, pois cada origem possui armazenamento separado; importe no novo endereço. Um volume Docker não muda esse comportamento.

## Portainer com Docker Swarm

Use **`stack.swarm.yml`** em vez de `compose.yaml`. A stack usa uma imagem pronta, sem `build`, compatível com nós Linux AMD64 e ARM64.

### 1. Aguarde a publicação da imagem

Abra a aba **Actions** deste repositório e aguarde o workflow **Publicar imagem Docker** terminar com sucesso. Ele executa os testes e publica:

`ghcr.io/andersondrt84/sistema-de-financas:latest`

Também existe uma tag com o SHA completo de cada commit, para fixar uma versão ou voltar à anterior. O workflow pode ser iniciado manualmente por **Run workflow**. As permissões `packages: write` usam o token automático do GitHub; não é preciso adicionar token aos arquivos.

### 2. Permita que o Swarm baixe a imagem

Na primeira publicação, o pacote GHCR pode ficar privado, mesmo que o repositório seja público. No GitHub, abra seu perfil → **Packages → sistema-de-financas → Package settings**. Se quiser permitir download sem login, altere a visibilidade do **pacote** para **Public**; isso publica a imagem da aplicação, não seus lançamentos financeiros.

Se preferir o pacote privado, adicione no Portainer um registry autenticado para `ghcr.io`, com usuário GitHub e token com `read:packages`, fornecido apenas no campo seguro do Portainer. Garanta que a autenticação do registry seja enviada aos nós durante o deploy. A autenticação Git para clonar repositório privado é separada da autenticação do registry.

### 3. Crie a stack pelo painel

No ambiente Swarm, abra **Stacks → Add stack → Repository**:

- Nome: `elo-financas`
- Repository URL: `https://github.com/andersondrt84/sistema-de-financas`
- Repository reference: `refs/heads/main`
- Compose path: **`stack.swarm.yml`**

Clique em **Deploy the stack**. Se preferir, use **Web editor** e cole o conteúdo de `stack.swarm.yml`. Aguarde o serviço ter **1/1 réplica** e a tarefa ficar saudável. A aplicação fica na porta **3080** de um nó do Swarm, através do routing mesh. Essa porta deve estar livre e acessível na rede do servidor. Para alterá-la, edite `published` na stack.

### Atualizações e diagnóstico

Após uma alteração em `main`, aguarde o workflow de publicação. No Portainer, atualize a stack/serviço solicitando novo download da imagem (re-pull). Publicar uma nova imagem não atualiza automaticamente os serviços em execução. Para versões fixas, substitua `latest` pelo SHA de uma publicação concluída.

Se a tarefa ficar `Rejected` com erro de pull, confira publicação da imagem e autenticação GHCR. Se a porta estiver ocupada, altere `published`. Se falhar o healthcheck, consulte os logs da tarefa. No manager, os comandos equivalentes são `docker stack services elo-financas`, `docker service ps elo-financas_elo --no-trunc` e `docker service logs elo-financas_elo`.

A configuração não pressupõe Traefik, domínio ou rede externa. Para usar seu proxy reverso, ajuste a rede e as regras conforme sua instalação. Os dados continuam no navegador; a stack não adiciona banco de dados ou sincronização.
