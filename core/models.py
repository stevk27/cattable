import enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Float, Integer, Numeric, String, func,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.enurations import UserRole
from database import Base
from sqlalchemy.orm import relationship
import uuid

############################################################################################################ 
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
    status = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    
    share_holder = relationship("ShareHolders", back_populates="user", uselist=False, foreign_keys='ShareHolders.user_id')
    admin_share_holders = relationship("ShareHolders", back_populates="created_by", foreign_keys='ShareHolders.created_by_id')


class Adresse(Base):
    __tablename__ = "adresse"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    longitude = Column(Float,nullable=True)
    latitude = Column(Float,nullable=True)
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
    company_name = Column(String(150),index=True)
    
    adresse_id = Column(UUID(as_uuid=True), ForeignKey('adresse.id'),nullable=True)
    adresse = relationship("Adresse",back_populates="company")
    
    share_insurance = relationship("ShareInsurance", back_populates="company")
    participation = relationship("Participation", back_populates="company")
    
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
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    user = relationship("User", back_populates="share_holder", foreign_keys=[user_id])

    # the user who have the admin status can create the shareholder
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    created_by = relationship("User", back_populates="admin_share_holders", foreign_keys=[created_by_id])

    
    attribution = relationship("Attribution",back_populates="share_holder")
    participation = relationship("Participation",back_populates="share_holder")
    
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
    company_id = Column(UUID(as_uuid=True),ForeignKey('company.id'),nullable = True)
    company = relationship("Company",back_populates='share_insurance')
    
    attribution = relationship("Attribution",back_populates="share_insurance")
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
    attribution = relationship("Attribution", back_populates="emission_certificate_file", uselist=False)
    created_at = Column(DateTime,server_default=func.now())


class Attribution(Base):
    __tablename__ = "attribution"

    id = Column(
        UUID(as_uuid=True),  
        primary_key=True,
        default=uuid.uuid4, 
        index=True
    )
    share_insurance_id = Column(UUID(as_uuid=True),ForeignKey("share_insurance.id"))
    share_insurance = relationship("ShareInsurance",back_populates='attribution')
    
    share_holder_id = Column(UUID(as_uuid=True),ForeignKey('share_holders.id'))
    share_holder = relationship("ShareHolders",back_populates="attribution")
    
    emission_certificate_file_id = Column(UUID(as_uuid=True), ForeignKey("file.id"))
    emission_certificate_file = relationship("File",back_populates="attribution")
    
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
    share_holder_id = Column(UUID(as_uuid=True),ForeignKey('share_holders.id'))
    share_holder = relationship("ShareHolders",back_populates="participation")

    company_id = Column(UUID(as_uuid=True),ForeignKey("company.id"),nullable=True)
    company = relationship("Company",back_populates="participation")
    
    total_share = Column(Integer,default=0)
    percentage_on_capital = Column(Float,nullable=True)
    created_at = Column(DateTime,server_default=func.now())

###################################################################################################################
############ Manage Log app ####################### 
class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    action = Column(String(255), nullable=False)  
    details = Column(String, nullable=True)  # Détails supplémentaires (ex: "Attribution de 50 parts à l'actionnaire...")
    created_at = Column(DateTime, server_default=func.now())

    # Relation avec l'utilisateur pour un affichage plus facile
    user = relationship("User")
