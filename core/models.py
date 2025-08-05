import enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, Numeric, String, func,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
from sqlalchemy.orm import relationship
import uuid

############################################################################################################ 
class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    status = Column(enum.Enum(UserRole), default=UserRole.USER)
    share_holder = relationship("ShareHolders", back_populates="user", uselist=False)
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

class Adresse(Base):
    __tablename__ = "adresse"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    longitude = Column(Column(Float),nullable=True)
    longitude = Column(Column(Float),nullable=True)
    city = Column(String(150),nullable=True)
    country = Column(String(150),nullable = True) 
    bp = Column(String(150),nullable = True)
    phone_number = Column(String(150),nullable = True)
    company = relationship("Company", back_populates="adresse", uselist=False)
    created_at = Column(DateTime,server_default=func.now())
    

class Company(Base):
    __tablename__ = "company"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    compagny_name = Column(String(150),index=True)
    adresse_id = Column(Integer, ForeignKey('adresse.id'))
    adresse = relationship("Adresse",back_populates="company")
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    

class ShareHolders(Base):
    __tablename__ = "share_holders"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    last_name = Column(String(150),index = True, nullable=True)
    first_name = Column(String(150) ,index = True, nullable=True)
    phone_number = Column(String(25),index = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User",back_populates="shareHolders")
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

class ShareInsurance(Base):
    __tablename__ = "share_insurance"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    company_id = Column(Integer,ForeignKey('company.id'))
    company = relationship("Company",back_populates='shareInsurance')
    number_of_share = Column(Integer,default=0)
    type_action = Column(String(100),nullable=True)
    unit_price = Column(Numeric(10, 3),default=0)
    created_at = Column(DateTime,server_default=func.now())

class File(Base):

    __tablename__ = "file"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    file_name = Column(String)
    storage_path = Column(String)
    type_of_file = Column(String(50),nullable=True)
    attribution = relationship("Attribution", back_populates="file", uselist=False)
    created_at = Column(DateTime,server_default=func.now())


class Attribution(Base):
    __tablename__ = "attribution"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    share_insurance_id = Column(Integer,ForeignKey("share_insurance.id"))
    share_insurance = relationship("ShareInsurance",back_populates='attribution')
    share_holder_id = Column(Integer,ForeignKey('share_holder.id'))
    share_holder = relationship("ShareHolder",back_populates="attribution")
    emission_certificate_file_id = Column(Integer,ForeignKey("file.id"))
    emission_certificate_file = relationship("file",back_populates="attribution")
    number_of_share = Column(Integer,default=0)
    
    attribution_date = Column(DateTime)
    created_at = Column(DateTime,server_default=func.now())

class Participation(Base):
    __tablename__ = "participation"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    share_holder_id = Column(Integer,ForeignKey('share_holder.id'))
    share_holder = relationship("ShareHolder",back_populates="attribution")

    company_id = Column(Integer,ForeignKey("company.id"))
    company = relationship("Company",back_populates="particiaption")
    total_share = Column(Integer,default=0)
    percentage_on_capital = Column(Float,nullable=True)
    created_at = Column(DateTime,server_default=func.now())


 
    