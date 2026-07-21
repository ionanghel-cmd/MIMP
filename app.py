from flask import Flask, render_template, redirect, url_for
from app.database import init_supabase
from app.routes.clients import clients_bp
from app.routes.orders import orders_bp
from app.routes.parts import parts_bp
from app.routes.dashboard import dashboard_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "CHANGE_ME_TO_A_RANDOM_SECRET"

# Initialize Supabase
init_supabase(app)

# Register Blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(clients_bp, url_prefix="/clients")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(parts_bp, url_prefix="/parts")


@app.route("/")
def home():
    return redirect(url_for("dashboard.dashboard"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
