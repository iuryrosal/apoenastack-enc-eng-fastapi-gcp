from fastapi import FastAPI
from apoena_api_fastapi.database.database_client import DatabaseClient
from apoena_api_fastapi.database.models import Customers
from sqlalchemy.orm import Session


app = FastAPI()


@app.get("/health_check")
async def health_check():
    return {"message": "Hello World!"}


@app.get("/customers/")
async def get_customers():
    database_client = DatabaseClient()
    with Session(database_client.engine) as session:
        results = session.query(Customers).all()
    return results
