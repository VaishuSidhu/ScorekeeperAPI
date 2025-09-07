
from . import db
from datetime import datetime

class Trader(db.Model):
    __tablename__ = "traders"
    id = db.Column(db.Integer, primary_key=True)
    traderName = db.Column(db.String(80), unique=True, nullable=False, index=True)
    score = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {"traderName": self.traderName, "score": self.score}

class TraderHistory(db.Model):
    __tablename__ = "trader_history"
    id = db.Column(db.Integer, primary_key=True)
    trader_id = db.Column(db.Integer, db.ForeignKey("traders.id"), nullable=False, index=True)
    prior_score = db.Column(db.Integer, nullable=False)
    new_score = db.Column(db.Integer, nullable=False)
    updated = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    trader = db.relationship("Trader", backref=db.backref("history", lazy=True))

    def to_dict(self):
        return {
            "traderName": self.trader.traderName if self.trader else None,
            "prior_score": self.prior_score,
            "new_score": self.new_score,
            "updated": self.updated,
            "timestamp": self.timestamp.isoformat() + "Z",
        }
