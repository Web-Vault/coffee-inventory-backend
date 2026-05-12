from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, engine, Base
import models
import schemas
import parser

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Route
@app.get("/")
def read_root():
    return {"message": "Welcome to BrewIQ API"}

# Simple API Test
@app.get("/api/test")
def test():
    return {"status": "API working"}

# Database Session Test
@app.get("/api/db-test")
def db_test(db: Session = Depends(get_db)):
    return {"db": "connected"}

# Product Query Test
@app.get("/api/products-test")
def products_test(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    return {
        "count": len(products)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)