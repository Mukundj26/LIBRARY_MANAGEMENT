from flask import Flask
from config import Config
from db import close_connection, init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register connection cleanup
    app.teardown_appcontext(close_connection)

    # Initialize SQLite database if it doesn't exist
    init_db(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.books import books_bp
    from routes.members import members_bp
    from routes.issues import issues_bp
    from routes.fines import fines_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(issues_bp)
    app.register_blueprint(fines_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
