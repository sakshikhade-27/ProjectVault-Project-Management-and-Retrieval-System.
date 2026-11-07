import os

from flask import Flask, flash, redirect, request, url_for

import config
from models import close_db, init_db
from routes.auth import auth_bp
from routes.categories import categories_bp
from routes.projects import projects_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    os.makedirs(os.path.dirname(config.DATABASE), exist_ok=True)
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

    app.teardown_appcontext(close_db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(projects_bp)

    @app.errorhandler(413)
    def file_too_large(_error):
        flash("That file is larger than 100 MB. Compress it or attach a smaller file.", "error")
        return redirect(request.referrer or url_for("projects.dashboard"))

    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
