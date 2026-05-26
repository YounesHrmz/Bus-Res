import core.db_handler as db

def get_all_buses():
    db.cur.execute("SELECT Bus_id, Bus_capacity, Bus_destination, Departure_time FROM buses")
    return db.cur.fetchall()

def get_bus_by_id(bus_id):
    db.cur.execute("SELECT Bus_id, Bus_capacity, Bus_destination, Departure_time FROM buses WHERE Bus_id = ?", (bus_id,))
    return db.cur.fetchone()
#check valid bus capacity and valid destination and  
def add_bus(capacity, destination, departure_time):
    if capacity > 35 or capacity < 25 :
        return False , "Bus Capacity must be between (35-25)"
    db.Add_Bus(capacity, destination, departure_time)

def delete_bus(bus_id):
    db.Del_Bus(bus_id)
