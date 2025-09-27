import click, pytest, sys
from flask.cli import AppGroup
from datetime import datetime
from typing import Optional

from App.database import db, get_migrate
from App.models.driver import Driver
from App.models.resident import Resident
from App.models.street import Street
from App.models.route import Route
from App.models.stop_request import StopRequest
from App.models.notification import Notification
from App.main import create_app
from App.controllers import initialize

app = create_app()
migrate = get_migrate(app)

# ---------- Helpers ----------
def parse_time(iso_string):
    """Convert ISO formatted string to datetime object (UTC)."""
    try:
        return datetime.fromisoformat(iso_string)
    except Exception:
        print("Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS")
        return None

def get_driver(driver_id: int) -> Optional[Driver]:
    return Driver.query.get(driver_id)

def get_resident(resident_id: int) -> Optional[Resident]:
    return Resident.query.get(resident_id)

def get_street(street_id: int) -> Optional[Street]:
    return Street.query.get(street_id)

def get_route(route_id: int) -> Optional[Route]:
    return Route.query.get(route_id)

# ---------- Init DB ----------
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print("Database initialized")

# ---------- Driver Commands ----------
driver_cli = AppGroup("driver", help="Driver related commands")

@driver_cli.command("create")
@click.argument("username")
@click.argument("password")
@click.option("--contact", default=None, help="Driver contact info")
def create_driver(username, password, contact):
    d = Driver(username=username, password=password, contact=contact)
    db.session.add(d)
    db.session.commit()
    print(f"Driver {d.username} created with id {d.id}")

@driver_cli.command("list")
def list_drivers():
    drivers = Driver.query.all()
    for d in drivers:
        print(f"ID={d.id}, Username={d.username}, Contact={d.contact}")

@driver_cli.command("schedule-route")
@click.option("--driver_id", required=True, type=int)
@click.option("--street_id", required=True, type=int)
@click.option("--time", required=True, type=str)
def schedule_route(driver_id, street_id, time):
    driver = get_driver(driver_id)
    street = get_street(street_id)
    if not driver or not street:
        print("Invalid driver or street")
        return
    route_time = parse_time(time)
    route = Route(driver_id=driver.id, street_id=street.id, scheduled_time=route_time)
    db.session.add(route)
    db.session.commit()
    print(f"Route scheduled: Driver {driver.username} -> {street.name} at {route_time}")

app.cli.add_command(driver_cli)

# ---------- Resident Commands ----------
resident_cli = AppGroup("resident", help="Resident related commands")

@resident_cli.command("create")
@click.argument("username")
@click.argument("password")
@click.option("--contact", default=None)
@click.option("--street_id", required=True, type=int)
def create_resident(username, password, contact, street_id):
    street = get_street(street_id)
    if not street:
        print("Invalid street ID")
        return
    r = Resident(username=username, password=password, contact=contact, street_id=street.id)
    db.session.add(r)
    db.session.commit()
    print(f"Resident {r.username} created with id {r.id} on {street.name}")

@resident_cli.command("list")
def list_residents():
    residents = Resident.query.all()
    for r in residents:
        street = Street.query.get(r.street_id)
        street_name = street.name if street else "None"
        print(f"ID={r.id}, Username={r.username}, Street={street_name}")

@resident_cli.command("view-inbox")
@click.option("--resident_id", required=True, type=int)
def view_inbox(resident_id):
    resident = get_resident(resident_id)
    if not resident:
        print("Resident not found")
        return
    routes = Route.query.filter_by(street_id=resident.street_id).all()
    if not routes:
        print("No scheduled routes for your street")
        return
    for route in routes:
        driver = Driver.query.get(route.driver_id)
        print(f"Route {route.id}: Driver={driver.username}, Time={route.scheduled_time}, Status={route.status}")

@resident_cli.command("request-stop")
@click.option("--resident_id", required=True, type=int)
@click.option("--route_id", required=True, type=int)
@click.option("--quantity", required=True, type=int)
@click.option("--notes", default="", type=str)
def request_stop(resident_id, route_id, quantity, notes):
    resident = get_resident(resident_id)
    route = get_route(route_id)
    if not resident or not route:
        print("Invalid resident or route")
        return
    req = StopRequest(resident_id=resident.id, route_id=route.id, quantity=quantity, notes=notes)
    db.session.add(req)
    db.session.commit()
    print(f"Stop request {req.id} created for {resident.username} on Route {route.id}")

app.cli.add_command(resident_cli)

# ---------- Route Commands ----------
route_cli = AppGroup("route", help="Route related commands")

@route_cli.command("list")
def list_routes():
    routes = Route.query.all()
    for route in routes:
        driver = Driver.query.get(route.driver_id)
        street = Street.query.get(route.street_id)
        print(f"Route {route.id}: Driver={driver.username}, Street={street.name}, Time={route.scheduled_time}, Status={route.status}")

@route_cli.command("set-status")
@click.option("--route_id", required=True, type=int)
@click.option("--status", required=True, type=click.Choice(["scheduled", "on the way", "arrived", "completed", "cancelled"]))
def set_status(route_id, status):
    route = get_route(route_id)
    if not route:
        print("Route not found")
        return
    old = route.status
    route.status = status
    db.session.commit()
    print(f"Route {route.id} status changed from {old} to {status}")

app.cli.add_command(route_cli)

# ---------- Test Commands ----------
test_cli = AppGroup("test", help="Run tests")

@test_cli.command("all")
def run_tests():
    sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test_cli)
