import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

SERVICE_ACCOUNT = os.path.join(os.path.dirname(__file__), "../../credentials/fiapyouvisa-478717-a432aa4af231.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_case(data):
    ref = db.collection("cases").document()
    data['created_at'] = datetime.now().isoformat()
    ref.set(data)
    return ref.id

def save_document(case_id, filename):
    ref = db.collection("cases").document(case_id).collection("documents").document()
    ref.set({"filename": filename, "timestamp": datetime.now().isoformat()})

def list_cases():
    return [dict(doc.to_dict(), id=doc.id) for doc in db.collection("cases").stream()]

def get_case_by_id(case_id):
    doc = db.collection("cases").document(case_id).get()
    if doc.exists:
        res = doc.to_dict()
        res['id'] = doc.id
        return res
    return {}

def update_case_status(case_id, status):
    db.collection("cases").document(case_id).update({"status": status})
