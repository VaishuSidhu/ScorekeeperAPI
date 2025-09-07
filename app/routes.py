
from flask import request, jsonify, current_app as app, Blueprint
from sqlalchemy import func
from flask_jwt_extended import jwt_required
from . import db, cache
from .models import Trader, TraderHistory

api_bp = Blueprint("api", __name__, url_prefix="/api")

def invalidate_leaderboard_cache():
    # Clear entire cache for simplicity; in prod, delete only leaderboard keys
    cache.clear()

@api_bp.route("/scores", methods=["POST"])
@jwt_required()
def add_or_update_score():
    data = request.get_json() or {}
    trader_name = data.get("traderName")
    score = data.get("score")

    if not trader_name or not isinstance(score, (int, float)):
        return jsonify({"error": "Invalid input: traderName (string) and score (number) required"}), 400

    score = int(score)

    trader = Trader.query.filter_by(traderName=trader_name).first()
    if trader is None:
        trader = Trader(traderName=trader_name, score=score)
        db.session.add(trader)
        db.session.flush()  # to get trader.id
        history = TraderHistory(trader_id=trader.id, prior_score=0, new_score=score, updated=True)
        db.session.add(history)
        db.session.commit()
        invalidate_leaderboard_cache()
        return jsonify(trader.to_dict()), 201
    else:
        prior = trader.score
        updated = False
        if score > trader.score:
            trader.score = score
            updated = True

        history = TraderHistory(trader_id=trader.id, prior_score=prior, new_score=score, updated=updated)
        db.session.add(history)
        db.session.commit()

        if updated:
            invalidate_leaderboard_cache()

        return jsonify(trader.to_dict()), 200

@api_bp.route("/leaderboard", methods=["GET"])
@cache.cached(timeout=60, query_string=True)  # cache per page/limit combo
def get_leaderboard():
    # Supports pagination: ?page=1&limit=10 ; defaults match the original Top 10
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "page and limit must be integers"}), 400

    if page < 1 or limit < 1 or limit > 100:
        return jsonify({"error": "page>=1, 1<=limit<=100"}), 400

    q = Trader.query.order_by(Trader.score.desc(), Trader.traderName.asc())
    traders = q.offset((page - 1) * limit).limit(limit).all()

    return jsonify([t.to_dict() for t in traders])

@api_bp.route("/rank/<string:traderName>", methods=["GET"])
def get_rank(traderName):
    trader = Trader.query.filter_by(traderName=traderName).first()
    if not trader:
        return jsonify({"error": "Trader not found"}), 404

    # Rank is 1 + number of traders with strictly greater score
    better_count = Trader.query.filter(Trader.score > trader.score).count()
    rank = better_count + 1
    return jsonify({"traderName": trader.traderName, "score": trader.score, "rank": rank})

@api_bp.route("/history/<string:traderName>", methods=["GET"])
def get_history(traderName):
    trader = Trader.query.filter_by(traderName=traderName).first()
    if not trader:
        return jsonify({"error": "Trader not found"}), 404
    # Most recent first
    events = TraderHistory.query.filter_by(trader_id=trader.id).order_by(TraderHistory.timestamp.desc()).all()
    return jsonify([e.to_dict() for e in events])

@api_bp.route("/stats", methods=["GET"])
def get_stats():
    total_traders = db.session.query(func.count(Trader.id)).scalar()
    highest_score = db.session.query(func.max(Trader.score)).scalar()
    average_score = db.session.query(func.avg(Trader.score)).scalar()
    return jsonify({
        "totalTraders": total_traders or 0,
        "highestScore": int(highest_score) if highest_score is not None else 0,
        "averageScore": round(float(average_score), 2) if average_score is not None else 0.0
    })
