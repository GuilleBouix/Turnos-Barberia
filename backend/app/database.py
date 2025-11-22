from flask_sqlalchemy import SQLAlchemy

# Creamos una instancia de SQLAlchemy sin pasarle la app
# Esto se llama "lazy initialization" y es el patrón recomendado
# La idea es no acoplar la BD directamente a la app, para poder usarla en múltiples contextos
db = SQLAlchemy()

# Con esto, en otros archivos hacemos:
# from app.database import db
# Y luego en app/__init__.py hacemos:
# db.init_app(app)
# Así separamos la config de la instancia de la app