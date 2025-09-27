# App/wsgi.py
import sys
import click
from datetime import datetime
from typing import Optional
import pytest

from flask.cli import AppGroup

from App.main import create_app
from App.database import db, get_migrate
from App.models.driver import Driver
from App.models.resident import Resident
from App.models.street import Street
from App.models.route import Route
from App.models.stop_request import StopRequest
from App.models.notification import Notification
from App.controllers.initialize import initialize  # ✅ Use absolute import

app = create_app()
migrate = get_migrate(app)

# -----------------------
# Helpers
# -----------------------
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

# -----------------------
# CLI Commands
# -----------------------
@app.cli.command("init", help="Creates and initializes the database")
def init():
    """Initialize the database with tables and sample data."""
    initialize()
    print("Database initialized")

# ---------- Driver Commands ----------
driver_cli = AppGroup("driver", help="Driver related commands")

@driver_cli.command("create")
@click.argument("username")
@click.argument("password")
@click.option("--contact", default=None, help="Driver contact info")
def create_driver_cli(username, password, contact):
    d = Driver(username=username, password=password, contact=contact)
    db.session.add(d)
    db.session.commit()
    print(f"Driver {d.username} created with id {d.id}")

@driver_cli.command("list")
def list_drivers_cli():
    drivers = Driver.query.all()
    for d in drivers:
        print(f"ID={d.id}, Username={d.username}, Contact={d.contact}")

app.cli.add_command(driver_cli)

# ---------- Resident Commands ----------
resident_cli = AppGroup("resident", help="Resident related commands")

@resident_cli.command("create")
@click.argument("username")
@click.argument("password")
@click.option("--contact", default=None)
@click.option("--street_id", required=True, type=int)
def create_resident_cli(username, password, contact, street_id):
    street = get_street(street_id)
    if not street:
        print("Invalid street ID")
        return
    r = Resident(username=username, password=password, contact=contact, street_id=street.id)
    db.session.add(r)
    db.session.commit()
    print(f"Resident {r.username} created with id {r.id} on {street.name}")

@resident_cli.command("list")
def list_residents_cli():
    residents = Resident.query.all()
    for r in residents:
        street_name = r.street.name if r.street else "None"
        print(f"ID={r.id}, Username={r.username}, Street={street_name}")

app.cli.add_command(resident_cli)

# ---------- Route Commands ----------
route_cli = AppGroup("route", help="Route related commands")

@route_cli.command("list")
def list_routes_cli():
    routes = Route.query.all()
    for route in routes:
        driver_name = Driver.query.get(route.driver_id).username if route.driver_id else "None"
        street_name = Street.query.get(route.street_id).name if route.street_id else "None"
        print(f"Route {route.id}: Driver={driver_name}, Street={street_name}, Time={route.scheduled_time}, Status={route.status}")

app.cli.add_command(route_cli)

# ---------- Test Commands ----------
test_cli = AppGroup("test", help="Run tests")

@test_cli.command("all")
def run_tests_cli():
    sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test_cli)
