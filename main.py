from fastapi import FastAPI, Depends # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session , engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,                   # Allow cookies/auth headers
    allow_methods=["*"],                      # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], 
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# products=[
#     Product(id=1,name="onkiieeee", rate=5000, desc="frontend devlouper"),
#     Product(id=2,name="hemant", rate=5000, desc="backend devlouper")
# ]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

# def init_db():
#     db = session()

#     count = db.query(database_models.Product).count()
#     if count ==0:
#         for product in Product:
#             db.add(database_models.Product(**product.model_dump()))
#         db.commit()

# init_db()


# read all Product
@app.get("/products")
def get_all_Product(db : Session = Depends(get_db)):    
    db_products = db.query(database_models.Product).all()
    return db_products


# read specific Product
@app.get("/products/{id}")
def getItem(id:int, db : Session = Depends(get_db)):
    db_products=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_products:
        return db_products
    return {"error": "Item not found"}

# insert new item 
@app.post("/products")
def additem(product : Product, db : Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    # for product in products:
    #     if product.name.lower() == item.name.lower():
    #         return "already exists"
    # products.append(item)
    db.commit()
    return {"message": "Item added successfully", "data": product}

# Update the product
@app.put("/products/{id}")
def update_item(id: int, product : Product, db : Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        # db_product.id=item.id
        db.commit()
        return "product updated"
    else:
        return "No product found"
    # for i in range(len(products)):
    #     if products[i].name == name:
    #         products[i]=item
    #         return "Item added successfully..."

@app.delete("/products/{id}")
def delete_item(id : int, db : Session = Depends(get_db)):
    db_products= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "product deleted..."
    else:
        return "Product deleted Successfully..."            
    # for i in range(len(products)):
    #     if products[i].name == name:
    #         del products[i]
    
    #         return "Item deleted successfully..."