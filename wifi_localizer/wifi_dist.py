import subprocess
import keyboard
import time

a = []

def list_nearby_wifi():

    result = subprocess.check_output(['nmcli', '-f', 'SSID,SIGNAL', 'dev', 'wifi', 'list']).decode()
    lines = result.strip().split('\n')
    lined = lines.pop(0)
     
    WifiList = []

    for line in lined:
        parts = line.strip().split()

        ssid = " ".join(parts[:-1])
        signal = int(parts[-1])
        WifiList.append((ssid, signal))

    return WifiList

while True:
    a = list_nearby_wifi()
    print(a)
    input()