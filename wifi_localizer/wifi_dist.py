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

def RecordLocation(wKnownsDict, locationName):
    scan_wifi()
    nearbyWifis = list_nearby_wifi()
    wKnownsDict[locationName] = nearbyWifis
    return wKnownsDict


def Locate(wKnownsDict):
    scan_wifi()
    nearbyWifis = list_nearby_wifi()
    
    # calculate closeness to each known location
    closeness = {}
    for location, wKnown in wKnownsDict.items():
        closeness[location] = Closeness(nearbyWifis, wKnown)
    
    # find the location with the minimum closeness
    closest_location = min(closeness, key=closeness.get)
    
    return closest_location

def signal_to_distance(signal_strength, k=1):
    return k * (100 - signal_strength)

def distance_between_wifi_signals(wifi_df: pd.DataFrame, k=1) -> dict:

    results = {}
    n = len(wifi_df)
    
    # Convert all signal strengths to distances first
    distances = {}
    for i in range(n):
        ssid = wifi_df.iloc[i]['ssid']
        signal = wifi_df.iloc[i]['signal_strength']
        distance = signal_to_distance(signal, k)
        distances[ssid] = distance
    
    # Calculate min and max ranges for each pair
    for i in range(n):
        ssid_i = wifi_df.iloc[i]['ssid']
        distance_i = distances[ssid_i]
        
        for j in range(i + 1, n):
            ssid_j = wifi_df.iloc[j]['ssid']
            distance_j = distances[ssid_j]
            
            dmin = abs(distance_i - distance_j)
            dmax = distance_i + distance_j
            
            key = tuple(sorted((ssid_i, ssid_j)))
            results[key] = (dmin, dmax)
    
    return results

if __name__ == "__main__":
    # Example usage
    wKnowns = {}
    # wKnowns = RecordLocation(wKnowns, "Home")
    # wKnowns = RecordLocation(wKnowns, "Work")
    # wKnowns = RecordLocation(wKnowns, "Cafe")

    wPrev = list_nearby_wifi()
    while True:
        scan_wifi()
        w = list_nearby_wifi()
        if  w.equals(wPrev): 
            print("not updated")
        else:
            print(w)
            wPrev = w
