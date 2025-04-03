from passlib.context import CryptContext

# Crear el contexto para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generar el hash de la contraseña 'admin'
hashed_password = pwd_context.hash("admin")

# Imprimir el hash generado
print("El hash generado para 'admin' es:")
print(hashed_password)
