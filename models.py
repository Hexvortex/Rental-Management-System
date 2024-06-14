from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base

class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    rent = Column(Float)
    water = Column(Float)
    electricity = Column(Float)
    wifi = Column(Float)
    tenants = relationship("Tenant", back_populates="house")

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    password = Column(String)
    house_id = Column(Integer, ForeignKey('houses.id'))
    house = relationship("House", back_populates="tenants")
    payments = relationship("Payment", back_populates="tenant")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    role = Column(String)  # 'caretaker' or 'tenant'

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    amount = Column(Float)
    type = Column(String)  # 'rent', 'water', 'electricity', 'wifi'
    status = Column(String)  # 'paid', 'partial', 'pending'
    remaining_amount = Column(Float, nullable=True)
    payment_code = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)
    tenant = relationship("Tenant", back_populates="payments")
