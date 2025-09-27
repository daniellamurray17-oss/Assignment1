from App.database import db
from datetime import datetime
from App.models.route import Route
from App.models.resident import Resident
from App.models.driver import Driver

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    route_id = db.Column(db.Integer, db.ForeignKey("route.id"), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey("residents.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)

    route = db.relationship("Route", back_populates="notifications")
    resident = db.relationship("Resident", back_populates="notifications")
    driver = db.relationship("Driver", back_populates="notifications")

    def get_json(self):
        return {
            "id": self.id,
            "resident_id": self.resident_id,
            "driver_id": self.driver_id,
            "message": self.message,
            "created_at": self.timestamp.isoformat() if self.timestamp else None
        }

    def __repr__(self):
        return f"<Notification id={self.id} resident_id={self.resident_id} driver_id={self.driver_id} route_id={self.route_id} message='{self.message}'>"
