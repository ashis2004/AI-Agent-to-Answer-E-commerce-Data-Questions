from sqlalchemy import (Boolean, Column, Date, Float, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

Base = declarative_base()

class ProductEligibility(Base):
    __tablename__ = "product_eligibility"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    eligibility_datetime_utc = Column(String(50), nullable=False)
    item_id = Column(Integer, nullable=False)
    eligibility = Column(Boolean, nullable=False)
    message = Column(String(500), nullable=True)

class ProductAdSales(Base):
    __tablename__ = "product_ad_sales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    item_id = Column(Integer, nullable=False)
    ad_sales = Column(Float, nullable=False)
    impressions = Column(Integer, nullable=False)
    ad_spend = Column(Float, nullable=False)
    clicks = Column(Integer, nullable=False)
    units_sold = Column(Integer, nullable=False)

class ProductTotalSales(Base):
    __tablename__ = "product_total_sales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    item_id = Column(Integer, nullable=False)
    total_sales = Column(Float, nullable=False)
    total_units_ordered = Column(Integer, nullable=False)

# Database engine and session
engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
