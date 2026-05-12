from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, engine, Base
import models
import schemas
import parser

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to BrewIQ API"}

@app.get("/api/test")
def test():
    return {"status": "API working"}

@app.get("/api/products-test")
def products_test(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    return {
        "count": len(products)
    }

# CREATE PRODUCT
@app.post("/api/products")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    existing_product = db.query(models.Product).filter(
        models.Product.sku == product.sku
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists"
        )

    new_product = models.Product(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# GET ALL PRODUCTS
@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):

    products = db.query(models.Product).all()

    return products


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)