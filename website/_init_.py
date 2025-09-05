from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "8=F&9w4Z{F"

    @app.errorhandler(404)
    def error_404(error):
        return render_template("error_404.html")

    from .auth import auth

    app.register_blueprint(auth, url_prefix="/")

    return app
