from flask import Flask

import models  # noqa: F401
from app.routes.api.v1 import api_v1
from database import init_db, db_session

app = Flask(__name__)
app.register_blueprint(api_v1)


@app.get("/health")
def health():
    return "Status ok", 200


@app.teardown_appcontext
def shutdown_session():
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run("0.0.0.0", port=3000, debug=True)
