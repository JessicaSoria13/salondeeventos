from sqlalchemy import Column, BigInteger, String, DateTime
from database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id")
    firstName = Column(String(255), name="first_name")  
    lastName = Column(String(255), name="last_name") 
    email = Column(String(255), name="email")
    phoneNumber = Column(String(255), name="phone_number") 
    registrationDate = Column(DateTime, name="registration_date", default=datetime.now)