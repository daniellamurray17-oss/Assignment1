from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from App.models import Driver, Resident
from App.database import db

def login(username, password):
    """
    Try to log in either a Driver or a Resident.
    """
    # First check Driver
    driver_result = db.session.execute(db.select(Driver).filter_by(username=username))
    driver = driver_result.scalar_one_or_none()
    if driver and driver.check_password(password):
        return create_access_token(identity=f"driver:{driver.id}")

    # Then check Resident
    resident_result = db.session.execute(db.select(Resident).filter_by(username=username))
    resident = resident_result.scalar_one_or_none()
    if resident and resident.check_password(password):
        return create_access_token(identity=f"resident:{resident.id}")

    return None


def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        # identity is already a string like "driver:1" or "resident:3"
        return identity

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]  # e.g. "driver:1"
        if not identity or ":" not in identity:
            return None
        role, id_str = identity.split(":")
        try:
            user_id = int(id_str)
        except ValueError:
            return None

        if role == "driver":
            return db.session.get(Driver, user_id)
        elif role == "resident":
            return db.session.get(Resident, user_id)
        return None

    return jwt


def add_auth_context(app):
    """
    Make 'is_authenticated' and 'current_user' available to all templates.
    """
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()  # e.g. "resident:2"
            if not identity or ":" not in identity:
                return dict(is_authenticated=False, current_user=None)

            role, id_str = identity.split(":")
            user_id = int(id_str)
            current_user = None

            if role == "driver":
                current_user = db.session.get(Driver, user_id)
            elif role == "resident":
                current_user = db.session.get(Resident, user_id)

            is_authenticated = current_user is not None
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None

        return dict(is_authenticated=is_authenticated, current_user=current_user)
