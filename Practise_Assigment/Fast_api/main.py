from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
import database_model
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_model.Base.metadata.create_all(bind = engine)

@app.get("/")
def greet():
    return "welcome to backend"

products = [
    Product(id=1, name="Laptop", description="Budget laptop", price=2300, quantity=10),
    Product(id=2, name="Smartphone", description="Android smartphone", price=1200, quantity=25),
    Product(id=3, name="Headphones", description="Wireless headphones", price=300, quantity=40),
    Product(id=4, name="Keyboard", description="Mechanical keyboard", price=150, quantity=30),
    Product(id=5, name="Mouse", description="Wireless mouse", price=80, quantity=50)
]

def get_db():
    db = session()
    try:
        yield db 
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_model.Product).count()
    if count == 0:
        for product in products:
                db.add(database_model.Product(**product.model_dump()))
    db.commit()

init_db()

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products = db.query(database_model.Product).all()
    # db connections 
    # querry data   
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
   db_products = db.query(database_model.Product).filter(database_model.Product.id == id).first()
   if db_products:
    return db_products
   return "product not found"

@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
   db_products = db.query(database_model.Product).filter(database_model.Product.id == id).first()
   if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        return "update successfully"
   else:
       return "No product found "

@app.delete("/products")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_products = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "delete successfully"
    return "Unable to delete"
