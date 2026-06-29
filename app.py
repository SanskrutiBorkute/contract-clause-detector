from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Ensure required runtime folders exist in the workspace
os.makedirs(os.path.join(app.root_path, "uploads"), exist_ok=True)
os.makedirs(os.path.join(app.root_path, "reports"), exist_ok=True)

# Register routes blueprints
from routes.analyzer import analyzer_bp
from routes.reports import reports_bp

app.register_blueprint(analyzer_bp)
app.register_blueprint(reports_bp)

@app.route("/")
def home():
    return render_template("clauseguard.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Run the server in debug mode locally
    app.run(host="0.0.0.0", port=port, debug=True)