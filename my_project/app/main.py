from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from market import fetch_cryptocurrencies

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Crypto(Base):
    __tablename__ = "cryptos"

    name = Column(String, primary_key=True)
    abreviature = Column(String)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

class cryptoResponse(BaseModel):
    name: str
    symbol: str
    price: float

def saveCryptoCurrencies(db, data):
    for item in data['data']:
        crypto = Crypto(
            name=item['name'],
            abreviature=item['abreviature'],
            price=item['quote']['USD']['price']
        )
        db.add(crypto)
    db.commit()


@app.get('/cryptos', response_model=list[cryptoResponse])
async def get_cryptocurrencies():
    db= SessionLocal()
    try:
        data = fetch_cryptocurrencies()
        saveCryptoCurrencies(db, data)
        crypto_data = [
            {
                'name': item['name'],
                'abreviature': item['abreviature'],
                'price': item['quote']['USD']['price']
            } for item in data['data']
        ]
        return crypto_data
    
    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()     