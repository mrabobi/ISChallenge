import time
import traceback

from librs import dblib as db
from flask import Flask

from google.cloud import logging

app = Flask(__name__)

logger = None

def init_logging():
    global logger
    logging_client = logging.Client()
    logger = logging_client.logger(__name__)
    logger.log_text("Created logger")


@app.route("/get", methods=["GET"])
def handle_get_resources(request):
    data = request.get_json()
    if 'resource_name' in data and data['resource_name'] == "location_name":
        if 'value' in data:
            return db.get_coords(data['value'])

    return {
        "msg": "Invalid request (Invalid JSON)",
        "status": 403
    }, 403


@app.route("/palatul_culturii")
def get_palat():
    li = list()
    #SELECT latitude, longitude, url, name FROM locations
    result, msg = db.get_everything_from_locations()
    for i in range(len(result)):
        result[i][2] = result[i][2].split(b"=")[1]
    return str(result)
    #return render_template("palat.html")
    

@app.route("/")
def index():
    # db.insert_new_location(47.15739, 27.58695, "Palatul Culturii",
    #                        "https://www.youtube.com/watch?v=eHT5ivcpeYI", "Palatul de langa Mall")
    # user = db.get_user_id("Daniel")
    # location = db.get_location_id("Palatul Culturii")
    # if user and location:
    #     db.user_add_new_challange(user, location)
    logger.log_text("Hello world!")
    return "Hello World!"


if __name__ == "__main__":
    init_logging()
    app.run(host="127.0.0.1", port=8080, debug=True)
