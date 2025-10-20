import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Personaje, Planeta, Favoritos

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
MIGRATE = Migrate(app, db)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response"}), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    personajes = Personaje.query.all()
    return jsonify([p.serialize() for p in personajes]), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify([p.serialize() for p in planetas]), 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.serialize() for u in usuarios]), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = Personaje.query.get_or_404(personaje_id)
    return jsonify(personaje.serialize()), 200

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = Planeta.query.get_or_404(planeta_id)
    return jsonify(planeta.serialize()), 200

@app.route('/personajes', methods=['POST'])
def crear_personaje():
    body = request.get_json()
    nuevo = Personaje(nombre=body.get("nombre"))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.serialize()), 201

@app.route('/planetas', methods=['POST'])
def crear_planeta():
    body = request.get_json()
    nuevo = Planeta(nombre=body.get("nombre"))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.serialize()), 201

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    body = request.get_json()
    nuevo = Usuario(nombre=body.get("nombre"))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.serialize()), 201

@app.route('/usuarios/<int:user_id>/favoritos', methods=['GET'])
def get_user_favorites(user_id):
    favoritos = Favoritos.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favoritos]), 200

@app.route('/favorite/personaje/<int:personaje_id>', methods=['POST'])
def add_favorite_personaje(personaje_id):
    user_id = request.args.get("user_id", type=int, default=1)
    nuevo_fav = Favoritos(user_id=user_id, personaje_id=personaje_id)
    db.session.add(nuevo_fav)
    db.session.commit()
    return jsonify({"msg": "Personaje añadido a favoritos"}), 201

@app.route('/favorite/planeta/<int:planeta_id>', methods=['POST'])
def add_favorite_planeta(planeta_id):
    user_id = request.args.get("user_id", type=int, default=1)
    nuevo_fav = Favoritos(user_id=user_id, planeta_id=planeta_id)
    db.session.add(nuevo_fav)
    db.session.commit()
    return jsonify({"msg": "Planeta añadido a favoritos"}), 201

@app.route('/favorite/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_favorite_personaje(personaje_id):
    user_id = request.args.get("user_id", type=int, default=1)
    fav = Favoritos.query.filter_by(user_id=user_id, personaje_id=personaje_id).first_or_404()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200

@app.route('/favorite/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_favorite_planeta(planeta_id):
    user_id = request.args.get("user_id", type=int, default=1)
    fav = Favoritos.query.filter_by(user_id=user_id, planeta_id=planeta_id).first_or_404()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
