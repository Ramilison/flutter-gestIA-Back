from typing import Optional
from pydantic import BaseModel

class Users(BaseModel):
    username: str
    lastname: str
    role: str
    email: str

class Supplier(BaseModel):
    uid: str
    fournisseurName: str
    fournisseurAdress: str
    nif: str
    stat: str
    contact: str
    dateCreation: str
    idSupplier: int

class Client(BaseModel):
    uid: str
    clientName: str
    clientSurname: str
    clientAdress: str
    nif: str = ""
    stat: str = ""
    contact: str
    mailAdress: str
    pro: int
    codeClient: str
    filePath: str = ""
    createdAt: Optional[str] = None
    idClient: int

class Unite(BaseModel):
    name: str
    unite: str
    idUnity: int

class CategorieProduits(BaseModel):
    name: str
    description: str
    idCategorie: int
    createdAt: Optional[str] = None

class Products(BaseModel):
    idProduct: int
    uid: str
    name: str
    description: str
    idCategorie: int
    idUnity: int
    unityName: str
    categoryName: str
    createdAt: Optional[str] = None


