import json
import geopy.distance

green_spaces = open('greenspace_w_access.geojson')
data_zones = open('zones_w_data.geojson')

s = json.loads(green_spaces.read())
z = json.loads(data_zones.read())

allGreenSpaces = s["features"]
allDataZones = z["features"]

def getDistance(a,b):
    coords1 = (a[1], a[0])
    coords2 = (b[1], b[0])
    distance = geopy.distance.vincenty(coords1, coords2).m
    return distance

#add fields for green space distances
for dataZone in allDataZones:
    dataZone["greenSpaceDistance"] = {}
    #dataZone["greenSpaceDistance"]["greenSpaceID"] = "null"
    #dataZone["greenSpaceDistance"]["distance"] = 1000000

#return key of max valud in 3 item diectionary
def retrieveMax(dictionary):
    currentMax = ('null', 0)
    for (k,v) in dictionary.items:
        if v > currentMax[1]:
            currentMax = (k,v)
    return currentMax()

def minGreenspaceDistance(dictionary, greenspaceID, distance):
    if greenspaceID not in dictionary:
        if len(dictionary) < 3:
            dictionary[greenspaceID] = distance
            print("initial distance added to dict")
        else:
            maxDist = retrieveMax(dictionary)
            maxDistID = maxDist[0]
            maxDistValue = maxDist[1]
            if distance < maxDistValue:
                del dictionary[maxDistID]
                dictionary[greenspaceID] = distance
                print("max distance updated")
    else:
        currentDistance = dictionary[greenspaceID]
        if distance < currentDistance:
            dictionary[greenspaceID] = distance
            print("New shorter distance " + str(distance) + str (greenspaceID))

for greenSpace in allGreenSpaces:
    access_points = greenSpace["accessCoordinates"]["coordinates"]
    for point in access_points:
        for dataZone in allDataZones:
            centroid = dataZone["properties"]["centroidCoord"]["coordinates"]
            d = getDistance(point, centroid)
            minGreenspaceDistance(dataZone["greenSpaceDistance"], greenSpace["properties"]["gml_id"], d)


z["features"] = allDataZones
output = json.dumps(z)

zone_greenspace_distance = open("zone_greenspace_distance.geojson", 'w')
zone_greenspace_distance.write(output)
zone_greenspace_distance.close()
