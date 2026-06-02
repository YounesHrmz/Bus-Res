from datetime import datetime, timedelta
import core.db_handler as db


def _validate_name(name):
    if not name or not isinstance(name, str):
        return False
    return all(part.isalpha() for part in name.split())


def _validate_phone(phone):
    return phone.isdigit() and len(phone) == 10


def add_reservation(bus_id, first, middle, last, phone):
    if not (_validate_name(first) and _validate_name(middle) and _validate_name(last)):
        return False, "Names must contain letters only."

    if not _validate_phone(phone):
        return False, "Phone number must be exactly 10 digits."

    db.cur.execute(
        "SELECT Departure_time, Bus_capacity FROM buses WHERE Bus_id = ?", (bus_id,)
    )
    result = db.cur.fetchone()
    if not result:
        return False, "Bus does not exist."

    departure_time_str, capacity = result
    try:
        departure_time = datetime.strptime(departure_time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return False, "Invalid departure time format."

    now = datetime.now()
    if departure_time - now < timedelta(hours=48):
        return False, "Cannot reserve: less than 48 hours before departure."

    db.cur.execute("SELECT COUNT(*) FROM reservation WHERE Bus_id = ?", (bus_id,))
    if db.cur.fetchone()[0] >= capacity:
        return False, "Bus is full."

    db.cur.execute(
        """
        SELECT 1 FROM reservation
        WHERE Bus_id = ? AND First_name = ? AND Middle_name = ? AND Last_name = ? AND Phone_number = ?
    """,
        (bus_id, first, middle, last, phone),
    )
    if db.cur.fetchone():
        return False, "You already have a reservation for this bus."

    db.cur.execute(
        """
        INSERT INTO reservation (Bus_id, First_name, Middle_name, Last_name, Phone_number)
        VALUES (?, ?, ?, ?, ?)
    """,
        (bus_id, first, middle, last, phone),
    )
    db.con.commit()
    return True, "Reservation added successfully."


def delete_reservation(first, middle, last, phone):
    if not (_validate_name(first) and _validate_name(middle) and _validate_name(last)):
        return False, "Names must contain letters only."

    if not _validate_phone(phone):
        return False, "Phone number must be exactly 10 digits."

    db.cur.execute(
        """
        DELETE FROM reservation
        WHERE First_name = ? AND Middle_name = ? AND Last_name = ? AND Phone_number = ?
    """,
        (first, middle, last, phone),
    )

    if db.cur.rowcount == 0:
        db.con.commit()
        return False, "Reservation not found."

    db.con.commit()
    return True, "Reservation deleted successfully."
