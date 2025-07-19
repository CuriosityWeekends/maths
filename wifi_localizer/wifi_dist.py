import subprocess
import time
import pandas as pd

a = []

def list_nearby_wifi():

    result = subprocess.check_output(['nmcli', '-f', 'SSID,SIGNAL', 'dev', 'wifi', 'list']).decode()
    lines = result.strip().split('\n')
    lines.pop(0)
     
    WifiList = []

    for line in lines:
        parts = line.strip().split()

        ssid = " ".join(parts[:-1])
        signal = int(parts[-1])
        WifiList.append((ssid, signal))
    
    WifiList = pd.DataFrame(WifiList)
    return WifiList

while True:
    a = list_nearby_wifi()
    print(a)
    input()