from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde el archivo .env

#MONGO_URI = os.getenv("MONGO_URI")

# Establece la conexión a MongoDB
#client = MongoClient(MONGO_URI)
#db = client["evaluacionesDB"]  # Base de datos donde se guardarán los voluntarios
#voluntarios_collection = db["voluntarios"]  # Colección de voluntarios
