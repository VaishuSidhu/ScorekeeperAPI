from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this to any secret

jwt = JWTManager(app)

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "admin123":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg":"Bad username or password"}), 401

# Protected route
@app.route('/api/scores', methods=['POST'])
@jwt_required()
def add_score():
    current_user = get_jwt_identity()
    data = request.get_json()
    trader = data.get("traderName")
    score = data.get("score")
    return jsonify({
        "message": f"Score added for {trader} by {current_user}",
        "score": score
    })

if __name__ == "__main__":
    app.run(debug=True)
