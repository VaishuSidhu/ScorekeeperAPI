from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 30

db = SQLAlchemy(app)
jwt = JWTManager(app)
cache = Cache(app)

with app.app_context():
    db.create_all()

# ---------------- Database Model ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Trader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    traderName = db.Column(db.String(50), unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)

# ---------------- Routes ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201


@app.route('/api/scores', methods=['POST'])
@jwt_required()
def add_score():
    data = request.get_json()
    traderName = data.get("traderName")
    score = data.get("score")

    trader = Trader.query.filter_by(traderName=traderName).first()
    if trader:
        if score > trader.score:
            trader.score = score
    else:
        trader = Trader(traderName=traderName, score=score)
        db.session.add(trader)

    db.session.commit()
    cache.delete_memoized(leaderboard)  # clear cache when scores change
    return jsonify({"msg": "Score updated"})


@app.route('/api/leaderboard', methods=['GET'])
@cache.cached(timeout=30)  # cache for 30 seconds
def leaderboard():
    top_traders = Trader.query.order_by(Trader.score.desc()).limit(10).all()
    return jsonify([{"traderName": t.traderName, "score": t.score} for t in top_traders])


@app.route('/api/rank/<string:name>', methods=['GET'])
def rank(name):
    traders = Trader.query.order_by(Trader.score.desc()).all()
    for idx, t in enumerate(traders):
        if t.traderName == name:
            return jsonify({"traderName": t.traderName, "score": t.score, "rank": idx+1})
    return jsonify({"msg": "Trader not found"}), 404


if __name__ == "__main__":
    with app.app_context():  # <- create application context
        db.create_all()      # create SQLite tables
    app.run(debug=True)
