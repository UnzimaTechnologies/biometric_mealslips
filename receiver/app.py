from flask import Flask, request, jsonify
import datetime as dt
from mealslip.database import get_connection
from mealslip.config import settings

app = Flask(__name__)

@app.route('/hik-event', methods=['POST'])
def hik_event():
    try:
        data = request.get_json(force=True)
        if not data or 'AcsEvent' not in data:
            return jsonify({"status": "ignored"}), 200

        inserted = 0
        conn = get_connection()
        cursor = conn.cursor()

        for info in data.get('AcsEvent', {}).get('InfoList', []):
            person_name = info.get('personName') or ""
            first_name, last_name = (person_name.split(" ", 1) + ["", ""])[:2]
            employee_id = info.get('employeeNo') or info.get('cardNo') or info.get('personID')
            device_sn = info.get('serialNo') or info.get('deviceSerialNo') or info.get('deviceSN')
            device_name = info.get('deviceName') or info.get('ipAddress') or "Unknown"
            att_time_str = info.get('time') or info.get('dateTime') or info.get('eventTime')
            status = info.get('attendanceStatus', 'GRANTED')
            direction = "in" if info.get('minor') in [38, 39, 1] else "out"
            person_group = info.get('personGroup', "")

            if not device_sn or not employee_id:
                continue

            try:
                auth_datetime = dt.datetime.fromisoformat(att_time_str.replace("Z", "+00:00")) if att_time_str else dt.datetime.now()
            except:
                auth_datetime = dt.datetime.now()

            # Call your existing stored procedure
            cursor.execute("""
                EXEC dbo.sp_InsertAttLog ?,?,?,?,?,?,?,?,?
            """, (employee_id, first_name, last_name, person_group,
                  device_name, device_sn, auth_datetime, status, direction))
            inserted += 1

        conn.close()
        return jsonify({"status": "ok", "inserted": inserted}), 200

    except Exception as e:
        app.logger.error(f"[HikEvent Error] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500