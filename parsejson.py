import json
from pprint import pprint

## generate a list of all craigslist sites and their lat / lon locations

## you can download this file from 
## http://www.craigslist.org/about/areas.json

json_data=open('areas.json')
data = json.load(json_data)

outfile = "areas.tsv"
header = ["region","name","lat","lon","hostname","country"]

with open(outfile, "w") as f:

    line = "\t".join(header) + "\n"
    f.write(line)
    for el in data:
        row = [el["region"], el["name"], el["lat"], el["lon"], el["hostname"], el["country"]]

        line = "\t".join(row) + "\n"
        f.write(line)

json_data.close()
