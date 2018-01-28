import json

zones = open('data_zone_boundaries/processed_zoneboundaries.geojson')
cent = open('processed_zonecentroids.geojson')
health = open('healthdata.json')

z = json.loads(zones.read())
c = json.loads(cent.read())
h = json.loads(health.read())

allZones = z["features"]
allCentroids = c["features"]
allHealth = h


centroidCounter = 0
healthCounter = 0

for zone in allZones:
    for centroid in allCentroids:
        if zone["properties"]["DataZone"] == centroid["properties"]["DataZone"]:
            zone["properties"]["centroidCoord"] = {}
            zone["properties"]["centroidCoord"]["type"] = "Point"
            zone["properties"]["centroidCoord"]["coordinates"] = centroid["geometry"]["coordinates"]
            centroidCounter = centroidCounter + 1
            print(str(centroidCounter) + " Centroid added to " + str(zone["properties"]["Name"]))

for zone in allZones:
    for health in allHealth:
        if zone["properties"]["DataZone"] == health["DZ2011"]:
            zone["properties"]["SIMD16_Quintile"] = health["SIMD16_Quintile"]
            zone["properties"]["SIMD16_HB_Quintile"] = health["SIMD16_HB_Quintile"]
            healthCounter = healthCounter + 1
            print(str(healthCounter) + " Health data added to " + str(zone["properties"]["Name"]))

z["features"] = allZones
output = json.dumps(z)

zones_w_data = open('zones_w_data.geojson', 'w')
zones_w_data.write(output)
zones_w_data.close()
