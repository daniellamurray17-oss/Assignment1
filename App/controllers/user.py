from App.database import db
from App.models.driver import Driver
from App.models.resident import Resident
from App.models.street import Street

# ------------------------
# Driver Functions
# ------------------------

def create_driver(username, password, contact=None):
    """Create a new driver."""
    driver = Driver(username=username, password=password, contact=contact)
    db.session.add(driver)
    db.session.commit()
    return driver

def get_driver(driver_id):
    """Get driver by ID."""
    return Driver.query.get(driver_id)

def get_all_drivers():
    """Return all drivers."""
    return Driver.query.all()

def get_all_drivers_json():
    """Return all drivers as JSON list."""
    return [d.get_json() for d in Driver.query.all()]


# ------------------------
# Resident Functions
# ------------------------

def create_resident(username, password, contact=None, street_id=None):
    """Create a new resident."""
    if street_id:
        street = Street.query.get(street_id)
        if not street:
            raise ValueError(f"Street with id {street_id} does not exist")
    resident = Resident(username=username, password=password, contact=contact, street_id=street_id)
    db.session.add(resident)
    db.session.commit()
    return resident

def get_resident(resident_id):
    """Get resident by ID."""
    return Resident.query.get(resident_id)

def get_all_residents():
    """Return all residents."""
    return Resident.query.all()

def get_all_residents_json():
    """Return all residents as JSON list."""
    return [r.get_json() for r in Resident.query.all()]
