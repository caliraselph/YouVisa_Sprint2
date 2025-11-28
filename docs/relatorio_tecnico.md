# Relatório Técnico – YOUVISA (Sprint 2)

**Equipe:** Ana Beatriz Duarte Domingues (RM 560302) · Junior Rodrigues da Silva (RM 559451) · Carlos Emilio Castillo Estrada (RM 559855)

## 1. Resumo
Nesta sprint consolidamos um MVP funcional da plataforma cognitiva da YOUVISA. O backend em FastAPI orquestra o recebimento de documentos, classificação NLP baseada em regras, validação visual com OpenCV/PyPDF2, persistência configurável (Firestore real ou memória) e automação de e-mail via SMTP. O frontend em React + Vite oferece painel para upload, listagem de casos e chatbot web com respostas contextuais. A solução demonstra o pipeline de ponta a ponta exigido pelo desafio, pronta para evoluir com modelos de IA mais robustos.

## 2. Arquitetura do pipeline
- **Backend FastAPI:** expõe os endpoints `/upload`, `/chat`, `/cases` e `/health`, centralizando a lógica de negócios.
- **Pipeline de automação:**
  - *NLP*: classificação de documentos por heurísticas (passaporte, formulário, comprovante, foto, outros) prontas para expansão com modelos spaCy/transformers.
  - *Visão computacional*: validação leve de imagens (OpenCV) e PDFs (PyPDF2), garantindo formato aceito e estrutura mínima.
  - *RPA/SMTP*: envio de confirmação automática de recebimento/validação, com fallback em modo simulado quando credenciais não estão disponíveis.
- **Persistência:** wrapper que opera em memória por padrão e pode alternar para Firestore real mediante configuração de `.env`.
- **Frontend/Chatbot:** painel React consome os endpoints REST e apresenta chat simplificado que orienta o usuário, consulta status e guia o fluxo de upload.

## 3. Etapas de desenvolvimento
1. **Organização do repositório:** limpeza de artefatos, criação de `.gitignore` raiz, padronização de variáveis em `.env` e remoção de duplicidades no frontend.
2. **Refino do backend:** implementação do pipeline (upload, NLP, visão, persistência, e-mail), criação do endpoint `/chat` e testes automatizados com `pytest` (modo memória).
3. **Interface React:** criação do dashboard com formulário de upload, tabela de casos, consulta por ID e chatbot integrado ao backend.
4. **Documentação:** atualização do README, elaboração do fluxograma e consolidação deste relatório técnico.

## 4. Desafios e soluções
- **Segurança de credenciais:** migração para variáveis `.env` com fallback documentado, evitando exposição involuntária.
- **Compatibilidade offline:** armazenamento em memória garante que o protótipo funcione sem dependências externas, mantendo opção de Firestore real.
- **Validação de arquivos:** OpenCV e PyPDF2 foram adotados para assegurar estrutura mínima sem aumentar muito a complexidade.
- **Chatbot enxuto:** optou-se por respostas baseadas em regras para atender ao requisito de IA/NLP sem depender de APIs pagas.

## 5. Resultados obtidos
- Pipeline modular em produção local: upload → classificação → validação → persistência → e-mail.
- Painel React exibindo casos em tempo real e assistente cognitivo funcional.
- Testes automatizados garantindo saúde do endpoint `/health`, fluxo de upload e listagem.
- Documentação completa (README, fluxograma, relatório) e guia de execução.

## 6. Próximos passos
- Integrar modelos NLP e visão mais avançados (spaCy, CNNs) e incorporar IA generativa para respostas contextualizadas.
- Conectar canais reais (Telegram/WhatsApp) ao endpoint `/chat` e padronizar logs/auditoria.
- Implementar persistência definitiva (Firestore/Cloud SQL) com camada de reprocessamento e dashboards de monitoramento.
- Realizar deploy em ambiente cloud (GCP, AWS ou Azure) com pipelines CI/CD.
