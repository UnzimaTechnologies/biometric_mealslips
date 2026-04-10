import datetime as dt

MEAL_WINDOWS = {
    "Breakfast": ("05:00", "07:00"),
    "Lunch": ("12:00", "14:30"),
    "Dinner": ("17:00", "19:00"),
}

def get_meal_type(scan_time: dt.datetime):
    t = scan_time.time()
    for meal, (start, end) in MEAL_WINDOWS.items():
        s = dt.datetime.strptime(start, "%H:%M").time()
        e = dt.datetime.strptime(end, "%H:%M").time()
        if s <= t <= e:
            return meal
    return "Other"

def build_slip(emp_id, fname, lname, dept, device_name, device_serial, auth_time, status):
    meal = get_meal_type(auth_time)
    timestamp = auth_time.strftime("%Y-%m-%d %H:%M:%S")
    def fit(text, w=40): return str(text)[:w].ljust(w)
    lines = [""] * 2
    lines.extend([
        "------------------------------",
        " Trident College MEAL SLIP ",
        "------------------------------",
        f"Name: {fit(fname + ' ' + lname)}",
        f"ID: {fit(emp_id)}",
        f"Group: {fit(dept)}",
        f"Device: {fit(device_name)}",
        f"Serial: {fit(device_serial or 'N/A')}",
        f"Time: {fit(timestamp)}",
        f"Meal: {fit(meal)}",
        f"Status: {fit(status)}",
        "------------------------------"
    ])
    lines.extend([""] * 15)
    return "\n".join(lines)