import core.db_handler as db


def get_all_buses():
    db.cur.execute(
        "SELECT Bus_id, Bus_capacity, Bus_destination, Departure_time FROM buses"
    )
    return db.cur.fetchall()


def get_bus_by_id(bus_id):
    db.cur.execute(
        "SELECT Bus_id, Bus_capacity, Bus_destination, Departure_time FROM buses WHERE Bus_id = ?",
        (bus_id,),
    )
    return db.cur.fetchone()


def add_bus(capacity, destination, departure_time):
    if capacity < 25 or capacity > 35:
        return False, "Bus capacity must be between 25 and 35."
    db.Add_Bus(capacity, destination, departure_time)
    return True, "Bus added successfully."


def delete_bus(bus_id):
    db.Del_Bus(bus_id)
