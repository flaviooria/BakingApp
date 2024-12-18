from flask import Flask

from common.config.database import init_db, db_session
from routes.v1 import api_v1

app = Flask(__name__)
app.register_blueprint(api_v1)


@app.get("/health")
def health():
    return "Status ok", 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run("0.0.0.0", port=3000, debug=True)
