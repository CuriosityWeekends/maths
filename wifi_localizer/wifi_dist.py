import subprocess
import re

def get_wifi_strength(interface='wlp0s20f3'):
    try:
        result = subprocess.check_output(['iwconfig', interface]).decode()
        match = re.search(r'Signal level=(-?\d+) dBm', result)
        if match:
            signal_level = int(match.group(1))
            return signal_level
        else:
            return None
    except subprocess.CalledProcessError:
        return None
while True:
    print("Signal strength (dBm):", abs(get_wifi_strength("wlp0s20f3")))
