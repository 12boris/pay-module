
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from Invoice import SessionLocal, Invoice, engine

app = FastAPI()

# Модели для входных данных
class InvoiceCreate(BaseModel):
    user_id: str

class InvoiceUpdate(BaseModel):
    invoice_status: str

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Роуты FastAPI

@app.post("/add_invoice/")
def add_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    db_invoice = Invoice(user_id=invoice.user_id, invoice_status='start')
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return {"id": db_invoice.id, "user_id": db_invoice.user_id, "invoice_status": db_invoice.invoice_status}


@app.put("/update_invoice/{invoice_id}")
def update_invoice(invoice_id: int, invoice_update: InvoiceUpdate, db: Session = Depends(get_db)):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db_invoice.invoice_status = invoice_update.invoice_status
    db.commit()
    return {"id": db_invoice.id, "user_id": db_invoice.user_id, "invoice_status": db_invoice.invoice_status}


@app.get("/get_invoice/{invoice_id}")
def get_invoice_by_id(invoice_id: int, db: Session = Depends(get_db)):
    try:
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).one()
        return {"id": db_invoice.id, "user_id": db_invoice.user_id, "invoice_status": db_invoice.invoice_status}
    except:
        raise HTTPException(status_code=404)
