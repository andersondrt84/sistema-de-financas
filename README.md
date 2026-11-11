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

### Docker Swarm

`docker stack deploy` ignora `build`. O arquivo `compose.yaml` é destinado a Docker Standalone. Para Swarm, primeiro publique a imagem em um registry acessível por todos os nós e use uma stack com `image` apontando para ela; a imagem `sistema-de-financas:local` não é publicada automaticamente. A configuração final depende do registry e do proxy/rede do seu servidor.
