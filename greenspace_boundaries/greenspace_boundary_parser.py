import json

spaces = open('greenspaceswgs84.geojson')

test_json = '{"type": "FeatureCollection","name": "greenspaceswgs84", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": [{ "type": "Feature", "properties": { "gml_id": "id567A5CDC-8223-3675-E053-2362A00AB33E", "function": "Play Space", "distinctiveName1": null, "distinctiveName2": null }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -2.730023464199331, 56.215190305614193 ], [ -2.729706592516628, 56.214925062470563 ], [ -2.729017589150877, 56.21519444265099 ], [ -2.729750925344214, 56.215323449339124 ], [ -2.729890055176348, 56.215305557418127 ], [ -2.730023464199331, 56.215190305614193 ] ] ] ] } },{ "type": "Feature", "properties": { "gml_id": "id567A5D11-A454-3675-E053-2362A00AB33E", "function": "Religious Grounds", "distinctiveName1": "Pittenweem Church", "distinctiveName2": null }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -2.728735463980573, 56.213845624270903 ], [ -2.728598077853995, 56.213717234682782 ], [ -2.72815422721258, 56.213607541031934 ], [ -2.728019277826819, 56.213658559735954 ], [ -2.728154086285303, 56.213770163861298 ], [ -2.727599432263633, 56.213973247029003 ], [ -2.728060823456957, 56.214293619058232 ], [ -2.728786999251597, 56.214071913203753 ], [ -2.728824514013793, 56.214009698083942 ], [ -2.728735463980573, 56.213845624270903 ] ] ] ] } }, { "type": "Feature", "properties": { "gml_id": "id567A5CDC-8223-3675-E053-2362A00AB33E", "function": "Play Space", "distinctiveName1": null, "distinctiveName2": null }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [-2.988, 56.479],[-2.988, 56.479] ] ] ] } }]}'

l = json.loads(spaces.read())
t = json.loads(test_json)

#c = [ [ -2.728735463980573, 56.213845624270903 ], [ -2.728598077853995, 56.213717234682782 ], [ -2.72815422721258, 56.213607541031934 ], [ -2.728019277826819, 56.213658559735954 ], [ -2.728154086285303, 56.213770163861298 ], [ -2.727599432263633, 56.213973247029003 ], [ -2.728060823456957, 56.214293619058232 ], [ -2.728786999251597, 56.214071913203753 ], [ -2.728824514013793, 56.214009698083942 ], [ -2.728735463980573, 56.213845624270903 ] ]
c = [[-2.988, 56.479],[-2.988, 56.479]]

# checks if coordinates are in dundee city
def checkCoords(coords):
    withinRange = True
    for coord in coords:
        withinRange = withinRange and checkCoord(coord)
    return withinRange

def checkCoord(coord):
    return checkLong(coord[0]) and checkLat(coord[1])

def checkLat(lat):
    return lat > 56.449 and lat < 56.5112

def checkLong(long):
    return long > -3.1 and long < -2.8

def checkFunction(function):
        return function in ["Cemetery", "Religious Grounds", "Play Space", "Public Park Or Garden", "Playing Field"]


#def processCoordinates():

def checkDataPoint(dataPoint):
        validFunction = checkFunction(dataPoint["properties"]["function"])
        validCoords = checkCoords(dataPoint["geometry"]["coordinates"][0][0])
        return validFunction and validCoords

allFeatures = l["features"]
validFeatures = []

for feature in allFeatures:
    if checkDataPoint(feature):
        validFeatures.append(feature)

l["features"] = validFeatures
del l['crs']
output = json.dumps(l)

filteredspaces = open('processed_greenspaces.geojson', 'w')
filteredspaces.write(output)
filteredspaces.close()
