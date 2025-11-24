# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
YOUVISA – Plataforma Inteligente de Atendimento Multicanal

## Nome do grupo
Grupo 22

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/">Ana Beatriz Duarte Domingues</a>
- <a href="https://www.linkedin.com/in/jrsilva051/">Junior Rodrigues da Silva</a>
- <a href="https://www.linkedin.com/in/">Carlos Emilio Castillo Estrada</a>

# 🤖 **YOUVISA – Plataforma Inteligente de Atendimento Multicanal**
# 🚀 YOUVISA – Sprint 2

> Automatización inteligente para servicios consulares

---

## 📌 Descripción del Proyecto

YOUVISA optimiza servicios consulares con IA, RPA, NLP y visión computacional. Esta sprint integra backend, clasificación de documentos, validación visual, automatización de tareas, Firestore y un panel opcional para agentes.

---

## 🛠️ Tecnologías Utilizadas

| Módulo        | Tecnología           | Descripción                         |
|---------------|---------------------|-------------------------------------|
| Backend       | FastAPI + Python    | API REST y pipeline automatizado    |
| Persistencia  | Firestore           | Base de datos de documentos/casos   |
| IA / NLP      | Python (simulado)   | Clasificación de tipo documentario  |
| Visión        | Simulación/OpenCV   | Validación por extensión/nombre     |
| RPA / Email   | SMTP + Python       | Email automático al usuario         |
| Frontend      | React + Vite        | Panel agente (opcional)             |
| Control       | Git & GitHub        | Versionamiento y colaboración       |

---

## 📂 Estructura del Repositorio

src/
│
├─ backend/
│ ├─ app/ # Lógica FastAPI: pipeline modular
│ ├─ credentials/ # Credencial Firebase (no subir pública)
│ ├─ uploaded/ # Documentos recibidos
│ ├─ venv/ # Entorno virtual (ignorado por .gitignore)
│ ├─ requirements.txt
├─ frontend/ # Panel (React - opcional)
├─ docs/ # Capturas, diagrama, informe


---

## ⚡ Instalación y Ejecución

1. Clona el repo y entra al backend
git clone https://github.com/caliraselph/YouVisa_Sprint2.git
cd YouVisa_Sprint2/src/backend

2. Activa entorno virtual y dependencias
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

3. Agrega serviceAccount.json a /credentials
4. Ejecuta el servidor FastAPI
python -m uvicorn app.main:app --reload

Accede: http://127.0.0.1:8000/docs

---

## 📲 Pruebas de la plataforma

### Endpoints principales

| URL              | Método | Descripción                       |
|------------------|--------|-----------------------------------|
| `/health`        | GET    | Estado del backend                |
| `/upload`        | POST   | Sube y clasifica documento        |
| `/cases`         | GET    | Lista casos/procesos              |
| `/cases/{id}`    | GET    | Consulta caso específico          |

### Ejemplo de uso

1. Sube archivo documentario en `/upload`
2. Pipeline:
   - Clasificación NLP (simulada)
   - Validación visual (extensión/nombre; listo para OpenCV)
   - Registro automático en Firestore
   - Envío de email por SMTP
3. Consulta estado desde `/cases` y Firestore

---

## ✉️ Email Automático (RPA) – Configuración SMTP

1. En Gmail, activa verificación en dos pasos
2. Genera una App password ([Guía Google](https://support.google.com/accounts/answer/185833?hl=es))
3. Configura en `app/rpa/email.py`:
    ```
    sender = "tucorreo@gmail.com"
    app_password = "XXXXXXXXXXXXXXXX"
    ```

---

## 🕵️‍♂️ Panel Agente (Frontend React)

- Consulta `/cases`, `/cases/{id}` desde React (opcional)
- Si no implementado, muestra pruebas en Swagger UI y capturas

---

## 📝 Ejemplo de Evidencias

- Subida y clasificación en Swagger UI
- Email recibido
- Diagrama de arquitectura
- Consulta Firestore

Incluye tus imágenes en `/docs`.

---

## 🔗 Diagrama de Arquitectura
Usuario/Chatbot
      ↓
Backend FastAPI
      ↓
Pipeline: NLP → Visión → RPA (email)
      ↓
Firestore
      ↓
Panel agente / Swagger UI / Frontend

---

## 🚀 ** Plano de Desenvolvimento (Sprint 2)**

| Etapa | Fase | Principais Tarefas | Responsável |
| :-- | :-- | :-- | :-- |
| 1 | Backend API | Desenvolver os endpoints da API com FastAPI, seguindo o contrato de dados. | Junior Rodrigues |
| 2 | Banco de Dados | Modelar e implementar a lógica de acesso ao Google Firestore. | Carlos Emilio |
| 3 | Lógica do Chatbot | Criar as cadeias (chains) e prompts no LangChain para o Gemini Flash. | Junior Rodrigues |
| 4 | Automação (RPA) | Implementar as funções de RPA e conectá-las ao backend. | Ana Beatriz |
| 5 | Infra & Deploy | Criar o Dockerfile da aplicação e configurar o pipeline de deploy no Google Cloud Run. | Carlos Emilio |
| 6 | Painel & Documentação | Criar o painel do agente (Streamlit) lendo do Firestore e manter o README.md. | Ana Beatriz |

---
## 🧾 ** Histórico de Versões**

---
| Versão    | Data       | Descrição                                        |
| :-------- | :--------- | :----------------------------------------------- |
| **0.2.0** | 04/11/2025 | Refatoração da arquitetura para Google Cloud: Google Cloud Run, Google Firestore, FastAPI e LangChain com Gemini Flash. |
| **0.1.0** | 09/10/2024 | Criação do documento e definição da arquitetura. |

