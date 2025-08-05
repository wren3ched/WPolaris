from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class VaultItem(Base):
    __tablename__ = 'vault_items'

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True)
    encrypted_password = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='vault_items')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) #Cifrada
    vault_items = relationship('VaultItem', back_populates='user')

    encripytion_key = Column(String)


