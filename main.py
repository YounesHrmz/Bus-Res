from flask import Flask, render_template, request, redirect, url_for, flash
from core import buses, reservation

app = Flask(__name__)
app.secret_key = "secret123"
Dest_List = [
    'Aleppo' , 
    'Damascus' ,
    'Hama' , 
    'Idlib' ,
    'Tartous' , 
    'DeirEzzor' , 
    'AlHasakah' ,
    'Qamishli' ,
    'AsSuwayda' ,
    'Daraa',
    'DamascusCountrySide',
    'Homs',
    'Quneitra'
]
@app.route("/")
def index():
    all_buses = buses.get_all_buses()
    return render_template("index.html", buses=all_buses)

@app.route("/add_bus", methods=["GET", "POST"])
def add_bus():
    if request.method == "POST":
        capacity = request.form.get("capacity")
        destination = request.form.get("destination")
        departure_time = request.form.get("departure_time")

        if not capacity.isdigit():
            flash("Capacity must be a number.", "danger")
            return redirect(url_for("add_bus"))

        from datetime import datetime
        try:
            datetime.strptime(departure_time, "%Y-%m-%d %H:%M")
        except:
            flash("Invalid time format.", "danger")
            return redirect(url_for("add_bus"))

        buses.add_bus(int(capacity), destination, departure_time)
        flash("Bus added.", "success")
        return redirect(url_for("index"))

    return render_template("add_bus.html",Dist_List= Dest_List)

@app.route("/delete_bus/<int:bus_id>", methods=["POST"])
def delete_bus(bus_id):
    buses.delete_bus(bus_id)
    flash("Bus deleted.", "success")
    return redirect(url_for("index"))

@app.route("/reserve/<int:bus_id>", methods=["GET", "POST"])
def reserve(bus_id):
    bus = buses.get_bus_by_id(bus_id)
    if not bus:
        flash("Bus not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        first = request.form.get("first_name")
        middle = request.form.get("middle_name")
        last = request.form.get("last_name")
        phone = request.form.get("phone_number")

        ok, msg = reservation.add_reservation(bus_id, first, middle, last, phone)
        flash(msg, "success" if ok else "danger")
        if ok:
            return redirect(url_for("index"))

    return render_template("reserve.html", bus=bus)

@app.route("/cancel_reservation", methods=["GET", "POST"])
def cancel_reservation():
    if request.method == "POST":
        first = request.form.get("first_name")
        middle = request.form.get("middle_name")
        last = request.form.get("last_name")
        phone = request.form.get("phone_number")

        ok, msg = reservation.delete_reservation(first, middle, last, phone)
        flash(msg, "success" if ok else "danger")
        return redirect(url_for("cancel_reservation"))

    return render_template("cancel.html")

if __name__ == "__main__":
    app.run(debug=True)
