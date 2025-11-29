from fastapi import FastAPI, UploadFile, File, Form
import os

from app.pipeline.nlp import classificar_documento
from app.pipeline.vision import validar_documento
from app.rpa.email import enviar_confirmacion
from app.db.firestore import save_case, save_document, list_cases, get_case_by_id, update_case_status

app = FastAPI()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploaded")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_document(
    user_id: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    filename = file.filename
    content = await file.read()

    # 1. Guardar archivo localmente
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(save_path, "wb") as f:
        f.write(content)

    # 2. Clasificar documento
    tipo_doc = classificar_documento(filename)

    # 3. Validar documento (simulado)
    valido, respuesta = validar_documento(filename)
    status = "Recebido"
    if valido:
        status = "Validado"
    else:
        status = "Erro: " + respuesta

    # 4. Guardar en Firestore
    case_id = save_case({
        "user_id": user_id,
        "email": email,
        "status": status,
        "tipo_doc": tipo_doc
    })
    save_document(case_id, filename)
    update_case_status(case_id, status)

    # 5. Automatización simulada (envío email)
    enviar_confirmacion(email, tipo_doc, status)

    return {
        "case_id": case_id,
        "filename": filename,
        "tipo_doc": tipo_doc,
        "status": status,
        "msg": f"Documento {tipo_doc} - {status}. Notificación enviada."
    }

@app.get("/cases")
def get_cases():
    return list_cases()

@app.get("/cases/{case_id}")
def get_case(case_id: str):
    case = get_case_by_id(case_id)
    if not case:
        return {"error": "Caso não encontrado"}
    return case


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # solo para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
