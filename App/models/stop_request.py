from App.database import db
from datetime import datetime, timezone

class StopRequest(db.Model):
    __tablename__ = 'stop_requests'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    quantity = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="requested")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 

    route = db.relationship("Route", back_populates="stop_requests")
    resident = db.relationship("User", back_populates="stop_requests")
    

    def __repr__(self):
        return f"<StopRequest id={self.id} resident_id={self.resident_id} route_id={self.route_id} status={self.status}>"
