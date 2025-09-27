from App.database import db
from datetime import datetime, timezone

class StopRequest(db.Model):
    __tablename__ = "stop_requests"

    id = db.Column(db.Integer, primary_key=True)
    # other fields ...

    def get_json(self):
        return {   # <- must be indented!
            "id": self.id,
            "resident_id": self.resident_id,
            "route_id": self.route_id,
            "quantity": self.quantity,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

