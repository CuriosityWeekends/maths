from matplotlib import pyplot as plt
import subprocess
import time
import pandas as pd
import numpy as np
from mapping_algorithm import best_distance_from_ranges #Runn this from the OptimalProblem directory
from mds_plot import plot_from_distance_matrix, compute_full_distance_matrix
# from sklearn.manifold import MDS

plt.ion()

# decclare a constant for max distance
constDistMax = 202



def scan_wifi(wifi_interface='wlp3s0'):
    # run if config to identify the wifi interface name
    # run sudo iw dev wlp0s20f3 scan
    subprocess.run(["sudo", "iw", "dev", wifi_interface, "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.run(["nmcli", "dev", "wifi", "rescan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def list_nearby_wifi(include: list[str]=[]):

    result = subprocess.check_output(['nmcli', '-f', f'SSID,{','.join(include)},SIGNAL', 'dev', 'wifi', 'list']).decode()
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

def signal_to_distance_dict(wifi_df: pd.DataFrame, k=1) -> dict: # Also converts to dict
    n = len(wifi_df)
    distances = {}
    for i in range(n):
        ssid = wifi_df.iloc[i]['ssid']
        signal = wifi_df.iloc[i]['signal_strength']
        distance = signal_to_distance(signal, k)
        distances[ssid] = distance
    return distances

def distance_between_wifi_signals(distances=None,wifi_df: pd.DataFrame=None, k=1) -> dict:
    results = {}
    if distances is None:
        if wifi_df is None:
            raise ValueError("wifi_df must be provided if distances is None")
        n = len(wifi_df)
        distances = signal_to_distance_dict(wifi_df, k)
    else:
        n = len(distances)
        if wifi_df is None:
            wifi_df = pd.DataFrame({'ssid': list(distances.keys())})
    
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

def distance_matrix(data):
    labels = sorted(set([k for pair in data.keys() for k in pair]))
    n = len(labels)
    dist_matrix = np.zeros((n, n))

    for (a, b), d in data.items():
        i, j = labels.index(a), labels.index(b)
        dist_matrix[i, j] = d
        dist_matrix[j, i] = d # For symmetry

    return labels, dist_matrix

def NamesOrder(namesOrder, wifi_list):
    """Updates namesOrder list with new SSIDs from wifi_list"""
    for i in range(len(wifi_list)):
        ssid = wifi_list.iloc[i]['ssid']
        if ssid not in namesOrder:
            namesOrder.append(ssid)
    return namesOrder

def DistMatAppend(distMat, namesOrder, diffOrSum='diff'):
    """Expands distMat to include new SSIDs in namesOrder"""
    n = len(namesOrder)
    if distMat.shape[0] < n:
        if diffOrSum == 'diff':
            newDistMat =  np.zeros((n, n))
        else:
            newDistMat = constDistMax * np.ones((n, n))
        # newDistMat = np.zeros((n, n))
        newDistMat[:distMat.shape[0], :distMat.shape[1]] = distMat
        distMat = newDistMat
    return distMat

def DiffsAndSums(distances, namesOrder, distDiffs, distSums):
    """Updates distDiffs and distSums matrices with new distances"""
    n = len(namesOrder)
    for i in range(n):
        ssid_i = namesOrder[i]
        if ssid_i not in distances:
            continue
        dist_i = distances[ssid_i]
        for j in range(i + 1, n):
        # for j in range(i + 0, n):
            ssid_j = namesOrder[j]
            if ssid_j not in distances:
                continue
            dist_j = distances[ssid_j]
            distDiff = abs(dist_i - dist_j)
            distDiff = max([distDiffs[i, j], distDiff])
            distDiffs[i, j] = distDiff
            distDiffs[j, i] = distDiff
            distSum = dist_i + dist_j
            distSum = min([distSums[i, j], distSum])
            distSums[i, j] = distSum
            distSums[j, i] = distSum
    return distDiffs, distSums


all_ranges = []
namesOrder = []

distDiffs = np.zeros([0,0])
distSums = constDistMax * np.ones([0,0])

scan_wifi()
wifi_list = list_nearby_wifi()
# print("wifi list:", wifi_list)

namesOrder = NamesOrder(namesOrder, wifi_list)

distDiffs = DistMatAppend(distDiffs, namesOrder, diffOrSum='diff') 
distSums = DistMatAppend(distSums, namesOrder, diffOrSum='sum')

distances = signal_to_distance_dict(wifi_list, k=1) # Distances to routers from orgin

distDiffs, distSums = DiffsAndSums(distances, namesOrder, distDiffs, distSums)

if __name__ == "__main__":
    k = 0
    while True:
        print(k)
        k = k + 1
        scan_wifi()
        wifi_list = list_nearby_wifi()
        # print("wifi list:", wifi_list)

        namesOrder = NamesOrder(namesOrder, wifi_list)

        distDiffs = DistMatAppend(distDiffs, namesOrder, diffOrSum='diff') 
        distSums = DistMatAppend(distSums, namesOrder, diffOrSum='sum')

        distances = signal_to_distance_dict(wifi_list, k=1) # Distances to routers from orgin

        distDiffs, distSums = DiffsAndSums(distances, namesOrder, distDiffs, distSums)

        # distDiffs will be the minimum of the corresponding index from distDiffs and distSums.
        # distDiffs[i,j] = min([distDiffs[i,j], distSums[i,j])
        # this is to ensure noise makes the estimate converge to right value and save the loop from trapped in wrong minima
        distDiffs = np.min([distDiffs, distSums], axis=0)
        distSums = np.max([distDiffs, distSums], axis=0)

        distMeans = (distDiffs + distSums) / 2.0
        distErrs = (distSums - distDiffs) / 2.0

        def DfDist(dists, namesOrder):
            dfDist = pd.DataFrame(dists)
            dfDist.columns = namesOrder
            dfDist.index = namesOrder
            return dfDist

        dfDistMeans = DfDist(distMeans, namesOrder)
        # print(dfDistMeans.round())
        dfDistErrs = DfDist(distErrs, namesOrder)
        print(dfDistErrs)
        # dfDistDiff = pd.DataFrame(distDiffs)
        # dfDistDiff.index = namesOrder
        # dfDistDiff.columns = namesOrder

        plot_from_distance_matrix(distMeans, labels=namesOrder)
    
        # print(np.round(dfDistDiff),0)
        print("===============")

if __name__ == "__main__ ":
    all_ranges = []
    namesOrder = []
    distDiffs = np.zeros([0,0])
    distSums = np.zeros([0,0])


    while True:
        pointName = input("Enter Location Name to scan or type 'stop' to finish: ")
        if 'stop' in pointName.lower():
            break
        scan_wifi()
        wifi_list = list_nearby_wifi()
        print("wifi list:", wifi_list)

        namesOrder = NamesOrder(namesOrder, wifi_list)

        distances = signal_to_distance_dict(wifi_list, k=1) # Distances to routers from orgin



        # appe
        if pointName != '':
            all_ranges.append({(pointName, key): (value, value) for key, value in distances.items()})
        distances = distance_between_wifi_signals(distances=distances)
        all_ranges.append(distances)

    best_distances, uncertanity = best_distance_from_ranges(all_ranges)
    # Print results
    for pair, distance in best_distances.items():
        #print(f"{pair}: {distance}; Uncertanity: ±{uncertanity[pair]}")
        # We could implement a threshold here to remove uncertain distances
        #For example
        if uncertanity[pair] < 20:
            print(f"Accepted {pair} with distance {distance} ±{uncertanity[pair]}")
    
    labels, dist_matrix = distance_matrix(best_distances)
    plot_from_distance_matrix(compute_full_distance_matrix(dist_matrix), labels)
    plt.pause(0.1)
    
'''
if __name__ == "__main2__":
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
'''
