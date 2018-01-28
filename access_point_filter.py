import json

spaces = open('greenspace_boundaries/processed_greenspaces.geojson')
points = open('access_points/accesspoints.geojson')

s = json.loads(spaces.read())
p = json.loads(points.read())
#t = json.loads(test_json)

allSpaces = s["features"]
allPoints = p["features"]

# checks if coordinates are in dundee city
def checkCoord(point):
    coord = point["geometry"]["coordinates"]
    return checkLong(coord[0]) and checkLat(coord[1])

def checkLat(lat):
    return lat > 56.449 and lat < 56.5112

def checkLong(long):
    return long > -3.1 and long < -2.8

# keep only dundee access points for space/point matching
validPoints = []

for point in allPoints:
    if checkCoord(point):
        validPoints.append(point)

p["features"] = validPoints
del p['crs']
output = json.dumps(p)

filteredpoints = open('filtered_access_points.geojson', 'w')
filteredpoints.write(output)
filteredpoints.close()
points.close()

fpoints = open('filtered_access_points.geojson', 'r')
fp = json.loads(fpoints.read())
