from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, engine, Base
import models
import schemas
import parser

# Create FastAPI app
app = FastAPI()

# Create database tables automatically
models.Base.metadata.create_all(bind=engine)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROOT ROUTE
@app.get("/")
def read_root():
    return {"message": "Welcome to BrewIQ API"}

# SIMPLE TEST ROUTE
@app.get("/api/test")
def test():
    return {"status": "API working"}

# DATABASE CONNECTION TEST
@app.get("/api/db-test")
def db_test(db: Session = Depends(get_db)):
    return {"db": "connected"}

# PRODUCTS COUNT TEST
@app.get("/api/products-test")
def products_test(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    return {
        "count": len(products)
    }

# GET ALL PRODUCTS
@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    return products

# CREATE PRODUCT
@app.post("/api/products")
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):

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

# DASHBOARD ROUTE
@app.get("/api/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    products = db.query(models.Product).all()

    return {
        "stats": [],
        "operations": [],
        "recentOperations": [],
        "products": products,
        "forecast": [],
        "branches": [],
        "aiReplies": []
    }

# PARSER TEST ROUTE
@app.post("/api/parser/query")
def parse_query(query: dict):

    user_msg = query.get("message", "").strip()

    if not user_msg:
        return {"reply": "Please enter a message."}

    return {
        "reply": f"You said: {user_msg}"
    }

@app.get("/api/seed")
def seed_database(db: Session = Depends(get_db)):

        # Prevent duplicate seeding
        existing = db.query(models.Product).first()

        if existing:
            return {"message": "Database already seeded"}

        sample_products = [

            models.Product(
                sku="COF001",
                name="Coffee Beans",
                category="Beverage",
                category_color="brown",
                branch="Main",
                on_hand=50,
                unit="kg",
                forecast=100,
                rule="Standard",
                price="500",
                status="OK",
                status_color="green",
                progress=80
            ),

            models.Product(
                sku="MLK001",
                name="Milk",
                category="Dairy",
                category_color="blue",
                branch="Main",
                on_hand=20,
                unit="ltr",
                forecast=40,
                rule="Cold Storage",
                price="60",
                status="Low Stock",
                status_color="amber",
                progress=30
            ),

            models.Product(
                sku="SUG001",
                name="Sugar",
                category="Sweetener",
                category_color="white",
                branch="Main",
                on_hand=100,
                unit="kg",
                forecast=150,
                rule="Dry Storage",
                price="45",
                status="OK",
                status_color="green",
                progress=90
            )

        ]

        db.add_all(sample_products)

        db.commit()

        return {
            "message": "Database seeded successfully"
        }

# RUN APP
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)