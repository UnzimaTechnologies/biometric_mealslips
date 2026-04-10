import logging
import time
from mealslip.database import get_connection
from mealslip.policy import resolve_print_policy
from mealslip.slip_builder import build_slip
from mealslip.printer import print_slip
from mealslip.config import settings

log = logging.getLogger(__name__)

def run_worker():
    log.info("MealSlip Printer Worker started – Serial-first policy active.")
    conn = cursor = None

    while True:
        try:
            if not conn:
                conn = get_connection()
                cursor = conn.cursor()

            # Fetch pending slips
            cutoff = time.time() - (settings.COOLDOWN_MINUTES * 60)
            cursor.execute("""
                SELECT TOP 500
                    attlog_id, employee_id, first_name, last_name, person_group,
                    device_name, device_sn, auth_datetime, authentication_result
                FROM dbo.attlog
                WHERE meal_slip_printed = 0
                  AND direction = 'in'
                  AND authentication_result = 'GRANTED'
                  AND auth_datetime >= DATEADD(second, -?, GETDATE())
                ORDER BY auth_datetime ASC
            """, (settings.COOLDOWN_MINUTES * 60,))
            rows = cursor.fetchall()

            if not rows:
                time.sleep(settings.POLL_INTERVAL)
                continue

            for row in rows:
                attlog_id, emp_id, fname, lname, dept, device_name, device_serial, auth_dt, status = row
                should_print, printer, match_type = resolve_print_policy(device_serial, device_name)

                if should_print:
                    slip_text = build_slip(emp_id, fname, lname, dept, device_name, device_serial, auth_dt, status)
                    if print_slip(printer, slip_text):
                        # Mark as printed
                        cursor.execute("UPDATE dbo.attlog SET meal_slip_printed = 1 WHERE attlog_id = ?", attlog_id)
                        log.info(f"[PRINT SUCCESS] {match_type} | Serial={device_serial} → {printer}")
                    else:
                        log.error(f"[PRINT FAILED] {printer} | Serial={device_serial}")
                else:
                    log.info(f"[AUTH ONLY] Serial={device_serial} | Device={device_name}")

        except Exception as e:
            log.error(f"[Worker Error] {e}")
            time.sleep(5)
            if conn:
                try: conn.close()
                except: pass
            conn = cursor = None