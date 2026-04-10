import platform
import subprocess
import tempfile
import os
import logging

log = logging.getLogger(__name__)

def print_slip(printer_name: str, slip_text: str):
    system = platform.system()
    try:
        if system == "Windows":
            import win32print
            hPrinter = win32print.OpenPrinter(printer_name)
            win32print.StartDocPrinter(hPrinter, 1, ("MealSlip", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, slip_text.encode("utf-8", errors="ignore"))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            win32print.ClosePrinter(hPrinter)
        else:  # Linux / macOS - uses CUPS lp command
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                tmp.write(slip_text.encode("utf-8"))
                tmp_path = tmp.name
            try:
                subprocess.run(["lp", "-d", printer_name, "-o", "raw", tmp_path], check=True)
                log.info(f"Printed via CUPS to {printer_name}")
            finally:
                os.unlink(tmp_path)
        return True
    except Exception as e:
        log.error(f"Print failed on {printer_name}: {e}")
        return False