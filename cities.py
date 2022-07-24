import geonamescache

gc = geonamescache.GeonamesCache()
countries = gc.get_cities_by_name()
# print countries dictionary
a= 'israel'
if a.capitalize() in countries.keys():
    print(True)
# print(countries.keys())