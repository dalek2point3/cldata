import requests
from bs4 import BeautifulSoup
import os.path
import re

def cache_data(url, fname):

    if os.path.isfile(fname):
        print "data exists"
    else:
        page = requests.get(url)
        with open(fname, 'w') as f:
            f.write(page.text)

def load_data(fname):
    f = open(fname)
    soup = BeautifulSoup(f.read(),"html.parser")
    return soup

def check_rows(rows):
    print "-------------"
    print "found rows: " + str(len(rows))
    print "-------------"

def get_rows(soup):
    content = soup.select("div.content")[0]
    rows = soup.select("p.row")
    return rows

def parse_data(soup):

    rows = get_rows(soup)
    check_rows(rows)

    data = []


    for row in rows:
       ismap = "nomap"
       ispix = "nopic"

       if len(row.select(".maptag")) != 0:
           ismap = "map"

       if len(row.select("span.px")[0].select("span.p")) != 0:
           ispix = "pic"

       date = row.select("span.date")[0].text

       try:
           price = row.select("span.price")[0].text
       except IndexError:
           price = "NA"


## <p class="row" data-pid="4526693657"> <a class="i" data-id="0:00P0P_i3itTi5eQsI" href="/apa/4526693657.html"></a> <span class="star"></span> <span class="pl"> <span class="date">Jun 24</span> <a href="/apa/4526693657.html">2624 Niazuma Avenue South -- Highland Park, Birmingham AL 35205</a> </span> <span class="l2"> <span class="price">$795</span> / 2br -  <span class="pnr"> <small> (Highland Avenue South)</small> <span class="px"> <span class="p"> pic<span class="maptag" data-pid="4526693657">map</span></span></span> </span> <a class="gc" data-cat="apa" href="/apa/">apts/housing for rent</a> </span> </p>


       link = row.select("span.pl")[0].find(href=re.compile("html"))
       href = link['href']

       # title = link.text
       try:
           area = row.select("span.pnr")[0].find("small").text
       except AttributeError:
           area = "NA"

       gc = row.select("a.gc")[0].text

       data.append([row['data-pid'], ismap, ispix, date, price, gc, href, area])
           
    return data

def write_data(data, outfile, subdomain):
    
    with open(outfile, "w") as f:
        for item in data:
            item.append(subdomain)
            item = [x.strip("\t") for x in item]
            item = [x.strip(",") for x in item]
            line = "\t".join(x.encode('utf-8') for x in item) + "\n"
            
            f.write(line)

def main():
    
    subdomain = "bham"
    section = "hhh"
    step = 100
    directory = "data/"
    fname_stub = "-".join([subdomain, section, str(step)])
    ext = ".html"
    outfile = "test.tsv"

    url = "http://" + subdomain + ".craigslist.org/" + section + "/index" + str(step) + ".html#list"
    fname = directory + fname_stub + ext

    # cache_data(url, fname)
    soup = load_data(fname)
    data = parse_data(soup)
    write_data(data, outfile, subdomain)

if __name__ == "__main__":

    print "welcome"
    print "--------------"
    main()

