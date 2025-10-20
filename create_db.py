from sqlalchemy import create_engine

# Conexión sin contraseña usando el sistema de autenticación "peer"
engine = create_engine("postgresql:///postgres?host=/var/run/postgresql&port=5433")

with engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT")
    conn.execute("CREATE DATABASE example;")

print("Base de datos 'example' creada correctamente.")