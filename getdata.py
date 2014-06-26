import requests
from bs4 import BeautifulSoup
import os.path
import re
import csv

def cache_data(url, fname):

    if os.path.isfile(fname):
        print "data exists"
    else:
        page = requests.get(url)
        print "got file"
        with open(fname, 'w') as f:
            f.write(page.text.encode('utf-8'))

def load_data(fname):
    f = open(fname)
    soup = BeautifulSoup(f.read(),"html.parser")
    return soup

def check_rows(rows):
    ## print "found rows: " + str(len(rows))
    return len(rows)

def get_rows(soup):

    try:
        content = soup.select("div.content")[0]
    except IndexError: # no data found
        return "Error"

    rows = soup.select("p.row")

    if(check_rows(rows)==0):
        return "Error"

    return rows

def parse_data(soup):

    rows = get_rows(soup)

    if rows == "Error":
        return "Error"

    data = []

    for row in rows:
       ismap = "nomap"
       ispix = "nopic"

       if len(row.select(".maptag")) != 0:
           ismap = "map"

       if len(row.select("span.px")[0].select("span.p")) != 0:
           ispix = "pic"

       try:
           date = row.select("span.date")[0].text
       except IndexError:
           date = "NA"

       try:
           price = row.select("span.price")[0].text
       except IndexError:
           price = "NA"


       link = row.select("span.pl")[0].find(href=re.compile("html"))
       href = link['href']
       # title = link.text

       try:
           area = row.select("span.pnr")[0].find("small").text
       except AttributeError:
           area = "NA"

       try:
           section = row.select("a.gc")[0].text
       except IndexError:
           section = "NA"

       data.append([row['data-pid'], ismap, ispix, date, price, section, href, area])
           
    return data

def write_data(data, outfile, subdomain):

    print "writing " + outfile
    with open(outfile, "w") as f:
        for item in data:
            item.append(subdomain)
            item = [x.strip("\t") for x in item]
            item = [x.strip(",") for x in item]
            line = "\t".join(x.encode('utf-8') for x in item) + "\n"
            
            f.write(line)

def get_block(step, section, subdomain):

    ext = ".html"
    directory = "data/"
    outdirectory = "parsed/"

    fname_stub = "-".join([subdomain, section, str(step)])
    outfile = outdirectory + subdomain + "-" + str(step) + ".tsv"

    # url = "http://" + subdomain + ".craigslist.org/" + section + "/index" + str(step) + ".html#list"
    url = "http://"+subdomain+".craigslist.org/search/apa?s="+str(step)

    fname = directory + fname_stub + ext

    cache_data(url, fname)
    soup = load_data(fname)
    data = parse_data(soup)

    if data != "Error":
        write_data(data, outfile, subdomain)
        return 1
    else:
        return 0

def load_subd(areafile):
    with open(areafile) as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [row["hostname"] for row in reader]

def main():
    
    maxrange = 5
    section = "hhh"

    areas = load_subd("areas.tsv")
    # areas = ["eastco", "swva"]

    for area in areas:
        print "+++++++++++++++++++++++++++++++++"
        for x in range(0,maxrange):
            print "--------------"
            print "processing: " + area + " step:" + str(x*100)
            status = get_block(x*100, section, area)
            if status == 0:
                print "No content found, skipping ... "
                break

if __name__ == "__main__":

    print "welcome"
    print "--------------"
    main()

