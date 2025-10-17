from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine, Base
from models import Client
from schemas import ClientCreate, ClientUpdate, ClientResponse, DeleteResponse

Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Reservas API",
    description="API REST",
    version="1.0.0"
)

@app.get("/cliente", response_model=List[ClientResponse], tags=["Clientes"])
def get_clients(db: Session = Depends(get_db)):
    '''GET'''
    clients = db.query(Client).all()
    return clients

@app.post("/cliente", response_model=ClientResponse, status_code=201, tags=["Clientes"])
def save_client(client: ClientCreate, db: Session = Depends(get_db)):
    '''POST'''
    new_client = Client(
        firstName=client.firstName,
        lastName=client.lastName,
        email=client.email,
        phoneNumber=client.phoneNumber
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.get("/cliente/{id}", response_model=ClientResponse, tags=["Clientes"])
def get_client_by_id(id: int, db: Session = Depends(get_db)):
    '''GET by id'''
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente con ID {id} no encontrado")
    return client

@app.put("/cliente/{id}", response_model=ClientResponse, tags=["Clientes"])
def update_client_by_id(id: int, request: ClientUpdate, db: Session = Depends(get_db)):
    '''PUT'''
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente con ID {id} no encontrado")
    
    # Actualizar solo los campos proporcionados
    if request.firstName is not None:
        client.firstName = request.firstName
    if request.lastName is not None:
        client.lastName = request.lastName
    if request.email is not None:
        client.email = request.email
    if request.phoneNumber is not None:
        client.phoneNumber = request.phoneNumber
    
    db.commit()
    db.refresh(client)
    return client

@app.delete("/cliente/{id}", response_model=DeleteResponse, tags=["Clientes"])
def delete_client_by_id(id: int, db: Session = Depends(get_db)):
    '''DELETE by id'''
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        return DeleteResponse(message=f"Error al intentar eliminar cliente con ID {id}.")
    
    try:
        db.delete(client)
        db.commit()
        return DeleteResponse(message=f"Cliente con ID {id} eliminado correctamente.")
    except Exception as e:
        db.rollback()
        return DeleteResponse(message=f"Error al intentar eliminar cliente con ID {id}.")
    
    
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Sistema de Reservas API"
    }
