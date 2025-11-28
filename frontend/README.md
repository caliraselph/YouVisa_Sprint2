# YOUVISA – Frontend (React + Vite)

Dashboard leve utilizado na Sprint 2 para acompanhar o pipeline cognitivo:

- Upload de documentos vinculado ao backend FastAPI (`POST /upload`).
- Listagem de casos e consulta individual (`GET /cases`).
- Chatbot web consumindo o endpoint `/chat`.

## Executando

```bash
npm install
npm run dev
```

O projeto assume o backend em `http://127.0.0.1:8000`. Para alterar, crie um arquivo `.env` na pasta `frontend/` com `VITE_API_BASE=http://seu-servidor:8000`.

Mais detalhes sobre arquitetura, variáveis de ambiente e documentação extra estão no arquivo `../README.md`.
