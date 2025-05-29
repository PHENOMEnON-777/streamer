# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from urllib.parse import quote_plus
# from pydantic_settings import BaseSettings


# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path) 

# class Settings(BaseSettings):
    
    
#     DB_USER:str = os.getenv('MYSQL_USER')
#     DB_PASSWORD:str = os.getenv('MySQL_PASSWORD')
#     DB_NAME:str =  os.getenv('MySQL_DB')
#     DB_HOST:str = os.getenv('MySQL_SERVER')
#     DB_PORT:str = os.getenv('MySQL_PORT')
#     SQLALCHEMY_URL_DATABASE:str= f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    
#     SECRET_KEY:str = os.getenv( "SECRET_KEY","09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
#     ALGORITHM:str = os.getenv("ALGORITHM","HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES:int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30)
    
    
# def get_settings() -> Settings:
#     return Settings()
     
    
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    DB_USER: str = os.getenv('MYSQL_USER')
    DB_PASSWORD: str = os.getenv('MYSQL_PASSWORD')  
    DB_NAME: str = os.getenv('MYSQL_DB')
    DB_HOST: str = os.getenv('MYSQL_SERVER')
    DB_PORT: str = os.getenv('MYSQL_PORT')
    SQLALCHEMY_URL_DATABASE: str = f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
def get_settings() -> Settings:
    return Settings()