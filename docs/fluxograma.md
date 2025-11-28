# Fluxograma – Pipeline YOUVISA (Sprint 2)

```mermaid
graph TD
    A[Usuário / Chatbot Web] -->|Mensagem / Upload| B[FastAPI / Endpoint /upload]
    B --> C[NLP – Classificação por regras]
    B --> D[Validação Visual (OpenCV / PyPDF2)]
    C --> E[Atualiza status do caso]
    D --> E
    E --> F[(Persistência)]
    F -->|Modo firestore| F1[Google Firestore]
    F -->|Modo memory| F2[Armazenamento em memória]
    E --> G[Envio de e-mail SMTP]
    F --> H[Endpoint /cases]
    A -->|Consulta| I[Endpoint /chat]
    I --> H
    H --> A
```

- **Entrada:** usuários enviam documentos pelo painel ou chatbot.
- **Processamento:** arquivo é classificado via regras NLP e validado com OpenCV/PyPDF2.
- **Persistência:** por padrão, os dados ficam em memória; opcionalmente, Firestore real pode ser ativado via `.env`.
- **Resposta automática:** status consolidado dispara e-mail (real ou simulado) e é exibido no painel.
- **Consultas:** chatbot consome `/chat` para orientar e consultar status; tabela no frontend usa `/cases`.
