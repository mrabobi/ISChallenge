import os
import time
import traceback
from datetime import datetime

from sqlalchemy import create_engine, engine, text
from sqlalchemy import Table, Column, Integer, MetaData, ForeignKey, TIMESTAMP, String

cloud_sql_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
db = create_engine(
    engine.url.URL(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    ),
)


def insert_user(name, email, token=None):
    with db.connect() as conn:
        added_at_timestamp = int(time.time())
        added_at_formatted = datetime.fromtimestamp(added_at_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        stmt = text(
            "INSERT INTO users (name, email, added_at, token) VALUES (:name, :email, :added_at, :token)"
        )

        result = conn.execute(
            stmt, name=name, email=email, added_at=added_at_formatted, token=token
        )

    if result:
        return True

    return False


def user_add_new_challange(user_id, location_id):
    with db.connect() as conn:
        # Format -- 2020-01-01 10:10:10
        start_time_timestamp = int(time.time())
        start_time_formatted = datetime.fromtimestamp(start_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        stmt = text(
            "INSERT INTO picked (user_id, location_id, start_time) VALUES (:user_id, :location_id, :start_time)"
        )

        result = conn.execute(
            stmt, user_id=user_id, location_id=location_id, start_time=start_time_formatted
        )

    if result:
        return True

    return False


def insert_new_location(lat, long, name, url, description):
    with db.connect() as conn:
        stmt = text(
            "INSERT INTO locations (latitude, longitude, name, url, description)"
            " VALUES (:latitude, :longitude, :name, :url, :description)"
        )

        result = conn.execute(
            stmt, latitude=lat, longitude=long, name=name, url=url, description=description
        )

    if result:
        return True

    return False


def get_location_id(name):
    with db.connect() as conn:
        stmt = text(
            "SELECT location_id FROM locations WHERE name=:name"
        )

        result = conn.execute(
            stmt, name=name
        ).fetchone()

    if result:
        return result[0]

    return None


def get_user_id(name):
    with db.connect() as conn:
        stmt = text(
            "SELECT user_id FROM users WHERE name=:name"
        )

        result = conn.execute(
            stmt, name=name
        ).fetchone()

    if result:
        return result[0]

    return None


def get_coords(name):
    with db.connect() as conn:
        stmt = text(
            "SELECT latitude, longitude FROM locations WHERE name=:name"
        )

        result = conn.execute(
            stmt, name=name
        ).fetchone()

    if result:
        return result, "result is {}".format(result)

    return None, ""


def get_everything_from_locations():
    with db.connect() as conn:
        stmt = text(
            "SELECT latitude, longitude, url, name FROM locations"
        )

        result = conn.execute(stmt).fetchall()

        return result, "result is {}".format(result)