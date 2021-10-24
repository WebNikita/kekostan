import sys  
# для настройки баз данных 
from sqlalchemy import Column, ForeignKey, Integer, String  
  
# для определения таблицы и модели 
from sqlalchemy.ext.declarative import declarative_base  
  
# для создания отношений между таблицами
from sqlalchemy.orm import relationship  
  
# для настроек
from sqlalchemy import create_engine  
  
# создание экземпляра declarative_base
Base = declarative_base()  
  
class Users(Base):  
    __tablename__ = 'users'  
    
    id = Column(Integer, primary_key=True)  
    key = Column(String(250), nullable=False)  
    files = Column(String(), nullable=True)  
  
# создает экземпляр create_engine в конце файла  
engine = create_engine('sqlite:///main.db')  
  
Base.metadata.create_all(engine)