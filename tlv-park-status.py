import http.client, urllib.request, urllib.parse, urllib.error, base64, json

headers = {
}

params = urllib.parse.urlencode({
})

conn = http.client.HTTPSConnection('api.tel-aviv.gov.il')
conn.request("GET", "/parking/StationsStatus?%s" % params, "{body}", headers)
response = conn.getresponse()
data = response.read().decode()
ajson = json.loads(data)
for item in ajson:
    print(item['Name'][::-1])
conn.close()

