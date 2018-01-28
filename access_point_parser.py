import json

spaces = open('greenspace_boundaries/processed_greenspaces.geojson')
points = open('filtered_access_points.geojson')

s = json.loads(spaces.read())
p = json.loads(points.read())
#t = json.loads(test_json)

allSpaces = s["features"]
allPoints = p["features"]

for space in allSpaces:
    # strip first two characters from id for matching
    old_id = space["properties"]["gml_id"]
    new_id = old_id[2:]
    space["properties"]["gml_id"] = new_id
    # add space for access point coordinates
    space["accessCoordinates"] = {}
    space["accessCoordinates"]["type"] = "LineString"
    space["accessCoordinates"]["coordinates"] = []

# loop through places and access points, where ids match add access point coordinates to space
for point in allPoints:
    for space in allSpaces:
        if point["properties"]["refToGreenspaceSite"] == space["properties"]["gml_id"]:
            space["accessCoordinates"]["coordinates"].append(point["geometry"]["coordinates"])

for space in allSpaces:
    #assign a perimiter point as access point if no official access points
    if len(space["accessCoordinates"]["coordinates"]) == 0:
        space["accessCoordinates"]["coordinates"].append(space["geometry"]["coordinates"][0][0][0])

s["features"] = allSpaces
print(len(allSpaces))
print(len(allPoints))
output = json.dumps(s)

greenspace_w_access = open('greenspace_w_access.geojson', 'w')
greenspace_w_access.write(output)
greenspace_w_access.close()
