import requests
import time

locations = open('PfPR_population.csv')
datalines = locations.readlines()

for line in datalines[1:]:
    with open("translated" + '.csv', 'a') as outFile:

        try:
            splitted = line.split(',')
            print(splitted[0], splitted[2])
            search_item = splitted[0] + " " + splitted[2]
            ans = requests.get("http://locationiq.org/v1/search.php?key=969d36a817e3c1&format=json&q={}".format(search_item))
            ans = ans.json()
            lat = ans[0]['lat']
            lon = ans[0]['lon']
            data = ','.join([splitted[0], splitted[2], lat, lon])
            outFile.write(data + '\n')
        except:
            pass
        time.sleep(1)
