from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime
from app.fsm import get_transicoes_validas
from app.db_oracle import get_case, create_case, list_cases, save_file, update_case_status
from app.fsm import validar_transicao
from app.db_oracle import update_case_status
from app.notifications import notify_status_change
from app.chatbot import responder_status, generate_response, classify_intent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YouVisa API")

# Monta uploads/ para servir archivos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "project": "YouVisa"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), case_id: str = Form(...), user_id: str = Form(...)):
    """Upload archivo a caso existente"""
    os.makedirs("uploads", exist_ok=True)
    filepath = f"uploads/{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    save_file(case_id, file.filename, filepath, len(await file.read()))
    return {"filename": file.filename, "case_id": case_id, "path": filepath}

@app.post("/cases/")
async def create_new_case(user_id: str = Form(...), channel: str = Form(...), email: str = Form(...)):
    """Crea nuevo caso de visa"""
    case_id = create_case(user_id, channel, email)
    return {"case_id": case_id, "status": "RECEBIDO", "next_states": get_transicoes_validas("RECEBIDO")}

@app.get("/cases/")
async def list_all_cases():
    return list_cases()

#@app.get("/cases/{case_id}")
#async def get_case_by_id(case_id: str):
#    case = get_case(case_id)
#    if not case:
#        raise HTTPException(status_code=404, detail="Caso não encontrado")
#    case["next_states"] = get_transicoes_validas(case["status"])
#    return case

@app.get("/cases/{case_id}")
async def get_case_by_id(case_id: str):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")
    case["next_states"] = get_transicoes_validas(case["status"])
    return case

@app.post("/cases/{case_id}/status/")
async def update_status(case_id: str, status: str = Form(...)):
    """Actualiza status validando FSM"""
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")
    
    if not validar_transicao(case['status'], status):
        raise HTTPException(status_code=400, detail=f"Transição inválida. Next válidos: {get_transicoes_validas(case['status'])}")
    
    update_case_status(case_id, status)
    return {"case_id": case_id, "new_status": status, "message": "Atualizado!"}

# 1. NOTIFICATION (email)
@app.post("/cases/{case_id}/notify/")
async def notify(case_id: str):
    case = get_case(case_id)  # TU función Oracle existente
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")
    
    result = notify_status_change(
        email_to=case['email'],
        case_id=case_id,
        new_status=case.get('status', 'RECEBIDO')
    )
    return result

# 2. CHATBOT Status
from app.chatbot import responder_status  # Crea abajo

@app.post("/chat/status/")
async def chat_status(case_id: str = Form(...)):
    return responder_status(case_id)

@app.post("/chat/")
async def chat_full(case_id: str = Form(...), message: str = Form(...)):
    intent = classify_intent(message)
    return generate_response(case_id, intent, message)
 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)