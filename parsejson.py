import json
from pprint import pprint

json_data=open('cldir/areas.json')

data = json.load(json_data)
outfile = "areas.csv"
header = ["region","name","lat","lon","hostname","country"]

with open(outfile, "w") as f:

    line = "\t".join(header) + "\n"
    f.write(line)
    for el in data:
        row = [el["region"], el["name"], el["lat"], el["lon"], el["hostname"], el["country"]]

        #for k,v in el.iteritems():
        #    row.append(v.strip())
        
        line = "\t".join(row) + "\n"
        f.write(line)

json_data.close()
