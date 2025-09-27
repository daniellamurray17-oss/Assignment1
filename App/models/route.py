from App.database import db
from datetime import datetime, timezone

class Route(db.Model):
    __tablename__ = "route"
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("streets.id"), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="scheduled")
    current_lat = db.Column(db.Float, nullable=True)
    current_lng = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  

    driver = db.relationship("Driver", backref=db.backref("routes", lazy=True))
    street = db.relationship("Street", backref=db.backref("Route", lazy=True))

    def get_json(self):
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "street_id": self.street_id,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "status": self.status,
            "current_lat": self.current_lat,
            "current_lng": self.current_lng
        }

    def __repr__(self):
        return f"<Route id={self.id} driver_id={self.driver_id} street_id={self.street_id} time={self.scheduled_time} status={self.status}>"
