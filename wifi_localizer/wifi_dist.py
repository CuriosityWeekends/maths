import subprocess
import time
import pandas as pd
import numpy as np

a = []

def scan_wifi(wifi_interface='wlp0s20f3'):
    # run if config to identify the wifi interface name
    # run sudo iw dev wlp0s20f3 scan
    subprocess.run(["sudo", "iw", "dev", wifi_interface, "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.run(["nmcli", "dev", "wifi", "rescan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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
    
    wifiList = pd.DataFrame(WifiList)
    wifiList.rename(columns={0:"ssid", 1:"signal_strength"}, inplace=True)

    # remove duplicate SSIDs due to 2.4 and 5 GHz by combining duplicates and taking the mean signal stregth
    wifiList = wifiList.groupby('ssid', as_index=False)['signal_strength'].mean()

    return wifiList

def Closeness(wWhereYouAre, wKnown):
    # calculates a closeness measure with pythogras approach
    wCloseness = wKnown.merge(wWhereYouAre, on="ssid", how="left")
    wCloseness = wCloseness.fillna(0)
    closeness = wCloseness["signal_strength_y"] - wCloseness["signal_strength_x"]
    closeness = closeness ** 2
    closeness = closeness.sum() / len(closeness)
    closeness = np.sqrt(closeness)
    return closeness


wPrev = list_nearby_wifi()
while True:
    scan_wifi()
    w = list_nearby_wifi()
    if  w.equals(wPrev): 
        print("not updated")
    else:
        print(w)
        wPrev = w
        input()
