import json

from database_handler import *
from datetime import datetime
from math import ceil

date_format = '%Y-%m-%d %H:%M:%S.%f'


def park(request_data):
    print(request_data)
    number = request_data['number']

    if get_from_database({"_id": number}) is None:
        accept = {"type": "accept"}

        start_time = datetime.now().strftime(date_format)
        db = {"_id": number, "time": start_time}
        add_to_database(db)

        add_to_database(
            {"type": "log", "date": datetime.now(),
             "text": f"Parked car {number} successfully."})
        return accept, 200

    else:
        error = {"type": "error", "code": 1}  # car is already parked
        add_to_database(
            {"type": "log", "date": datetime.now(), "text": f"Sent error 1."})

        return error, 400


def unpark(request_data):
    try:
        number = request_data['number']

    except TypeError:
        error = {"type": "error", "code": 3} #wrong data
        return error, 401

    if get_from_database({"_id": number}) is not None:
        finish_time = datetime.now().strftime(date_format)

        start_time = get_from_database({"_id": number}).get("time", None)
        diff = datetime.strptime(finish_time, date_format) - datetime.strptime(start_time,
                                                                               date_format)
        amount = ceil(diff.seconds / 3600) * 100  # 100 = price per hour

        checkout = {"type": "checkout", "amount": amount}
        delete_from_database({"_id": number})

        db = {"type": "history", "number": number, "date": finish_time, "amount": amount}
        add_to_database(db)

        add_to_database(
            {"type": "log", "date": datetime.now(),
             "text": f"Unparked car {number} successfully."})

        return checkout, 200

    else:
        error = {"type": "error", "code": 2}  # car is not parked yet

        add_to_database(
            {"type": "log", "date": datetime.now(), "text": f"Sent error 2."})

        return error, 400


def log():
    data = get_from_database({"type": "log"}, multiple=True)
    data = json.dumps(data, default=str)
    return data, 200


def history():
    data = get_from_database({"type": "history"}, multiple=True)
    data = json.dumps(data, default=str)
    return data, 200

def total():
    total_amount = get_total_amount()[0].get('total', None)
    total = {"total": total_amount}
    return total, 200



