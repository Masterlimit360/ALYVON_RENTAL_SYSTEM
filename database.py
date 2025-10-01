"""
Database configuration and models for the rental management system.
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date

# Database configuration
from config import DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    """Items available for rental (chairs, tables, etc.)"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    total_quantity = Column(Integer, nullable=False, default=0)
    available_quantity = Column(Integer, nullable=False, default=0)
    daily_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    rentals = relationship("Rental", back_populates="item")

class Customer(Base):
    """Customer information"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    rentals = relationship("Rental", back_populates="customer")

class Rental(Base):
    """Rental transactions"""
    __tablename__ = "rentals"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, nullable=False)
    rental_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    daily_rate = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    is_returned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="rentals")
    item = relationship("Item", back_populates="rentals")

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize the database (no default items)"""
    create_tables()
    print("Database initialized - ready for your inventory items")
