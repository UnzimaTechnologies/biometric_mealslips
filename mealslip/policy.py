from mealslip.config import settings

def resolve_print_policy(device_serial: str, device_name: str):
    if device_serial:
        serial_norm = str(device_serial).strip().upper()
        if serial_norm in settings.DEVICE_PRINT_POLICY_SERIAL:
            return True, settings.DEVICE_PRINT_POLICY_SERIAL[serial_norm], "SERIAL"
    if device_name:
        name_norm = str(device_name).strip().lower()
        if name_norm in settings.DEVICE_PRINT_POLICY_NAME:
            return True, settings.DEVICE_PRINT_POLICY_NAME[name_norm], "NAME_FALLBACK"
    return False, None, None