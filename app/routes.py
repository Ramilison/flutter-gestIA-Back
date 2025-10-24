from typing import List
from urllib import request
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import Request
from multiprocessing.connection import Client
from app.firebase_config import db
from app.models import Products

router = APIRouter()

class LoginRequest(BaseModel):
    uid: str
    username: str
    lastname: str
    email: str
    role: str

@router.post("/login")
async def login_user(payload: LoginRequest):
    print(f"Connexion de l'utilisateur {payload.email}")
    return {"message": f"Bienvenue {payload.username}"}

@router.post("/users")
async def create_user(user: dict):
    try:
        db.collection("users").document(user["uid"]).set(user)
        return {"message": "Utilisateur ajouté depuis le backend"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/users")
async def get_users():
    try:
        users_ref = db.collection("users")
        docs = users_ref.stream()

        users = []
        for doc in docs:
            user = doc.to_dict()
            user["id"] = doc.id
            users.append(user)

        return {"users": users}
    except Exception as e:
        return {"error": str(e)}

@router.get("/fournisseurs")
async def get_fournisseurs():
    try:
        fournisseurs_ref = db.collection("fournisseurs")
        docs = fournisseurs_ref.stream()

        fournisseurs = []
        for doc in docs:
            fournisseur = doc.to_dict()
            fournisseur["id"] = doc.id
            fournisseurs.append(fournisseur)

        return {"fournisseurs": fournisseurs}
    except Exception as e:
        return {"error": str(e)}

@router.post("/fournisseurs")
async def add_fournisseur(fournisseur: dict):
    try:
        db.collection("fournisseurs").add(fournisseur)
        return {"message": "Fournisseur ajouté avec succès oooo"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/fournisseurs/user")
async def get_fournisseur_by_userID(request: Request):
    try:
        uid = request.query_params.get("uid")
        if not uid:
            raise Exception("UID manquant dans la requête")
        fournisseur = db.collection("fournisseurs").where("uid", "==", uid).get()
        if len(fournisseur) == 0:
            return {"message": "Aucun fournisseurs trouvé pour cet utilisateur"}
        fournisseur_list = []
        for response in fournisseur:
            client_data = response.to_dict()
            fournisseur_list.append(client_data)
        return {"supplier": fournisseur_list}
    except Exception as e:
        return {"error": str(e)}

    
@router.post("/client")
async def add_client(client: dict):
    try:
        db.collection("clients").add(client)
        return {"message": "Client ajouté avec succès"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
    

@router.get("/clients/user")
async def get_clients_by_userID(request: Request):
    try:
        uid = request.query_params.get("uid")
        if not uid:
            raise Exception("UID manquant dans la requête")
        clients = db.collection("clients").where("uid", "==", uid).get()
        if len(clients) == 0:
            return {"message": "Aucun client trouvé pour cet utilisateur"}
        client_list = []
        for client in clients:
            client_data = client.to_dict()
            client_list.append(client_data)
        return {"clients": client_list}
    except Exception as e:
        return {"error": str(e)}
    
        
@router.get("/clients")
async def get_iclients():
    try:
        clients_ref = db.collection("clients")
        docs = clients_ref.stream()

        clients = []
        for doc in docs:
            client = doc.to_dict()
            client["id"] = doc.id
            clients.append(client)

        return {"clients": clients}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/unite")
async def add_unite(unite: dict):
    try:
        db.collection("unite").add(unite)
        return {"message": "Unité ajouté avec succès"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@router.put("/unite/{idUnity}")
async def update_unite(idUnity: int, unite: dict):
    try:
        query = db.collection("unite").where("idUnity", "==", idUnity).limit(1)
        docs = query.stream()

        doc = next(docs, None)
        if not doc:
            return {"error": "Unité non trouvée"}

        doc_ref = db.collection("unite").document(doc.id)
        doc_ref.update({
            'name': unite['name'],
            'unite': unite['unite'],
            'idUnity': idUnity
        })
        return {"message": "Unité mise à jour avec succès"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


@router.get("/unite/user")
async def get_unite_by_userID(request: Request):
    try:
        uid = request.query_params.get("uid")
        if not uid:
            raise Exception("UID manquant dans la requête")
        unites = db.collection("unite").where("uid", "==", uid).get()
        if len(unites) == 0:
            return {"message": "Aucun unite trouvé pour cet utilisateur"}
        unite_list = []
        for unite in unites:
            unite_data = unite.to_dict()
            unite_list.append(unite_data)
        return {"unite": unite_list}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/category")
async def add_unite(category: dict):
    try:
        db.collection("category").add(category)
        return {"message": "Categoryité ajouté avec succès"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
    

@router.get("/category/user")
async def get_category_by_userID(request: Request):
    try:
        uid = request.query_params.get("uid")
        if not uid:
            raise Exception("UID manquant dans la requête")
        category = db.collection("category").where("uid", "==", uid).get()
        if len(category) == 0:
            return {"message": "Aucun category trouvé pour cet utilisateur"}
        response_list = []
        for response in category:
            response_data = response.to_dict()
            response_list.append(response_data)
        return {"category": response_list}
    except Exception as e:
        return {"error": str(e)}
        

@router.post("/products")
async def create_product(product: dict):
    try:
        db.collection("products").add(product)

        return { "message": "Product created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/user")
async def get_product_by_userID(request: Request):
    try:
        uid = request.query_params.get("uid")
        if not uid:
            raise Exception("UID manquant dans la requête")
        products = db.collection("products").where("uid", "==", uid).get()
        if len(products) == 0:
            return {"message": "Aucun cateproductsgory trouvé pour cet utilisateur"}
        response_list = []
        for response in products:
            response_data = response.to_dict()
            response_list.append(response_data)
        return {"products": response_list}
    except Exception as e:
        return {"error": str(e)}

@router.get("/products", response_model=List[Products])
async def get_products(idCategorie: str = None):
    try:
        products_ref = db.collection('products')
        
        if idCategorie:
            products_ref = products_ref.where('idCategorie', '==', idCategorie)
        
        products_snapshot = products_ref.stream()
        
        products = []
        for product_doc in products_snapshot:
            product_data = product_doc.to_dict()
            category_ref = db.collection('category').document(product_data['idCategorie'])
            category_doc = category_ref.get()
            
            if category_doc.exists:
                category_data = category_doc.to_dict()
                products.append(Products(
                    id=product_doc.id,
                    name=product_data['name'],
                    description=product_data['description'],
                    unityId=product_data['unityId'],
                    idCategorie=product_data['idCategorie'],
                    categoryName=category_data['name']
                ))
            else:
                raise HTTPException(status_code=404, detail="Category not found")

        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))










