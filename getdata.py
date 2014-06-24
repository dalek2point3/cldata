import requests
from bs4 import BeautifulSoup
import os.path

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
       ismap = 0
       if len(row.select(".maptag")) == 0:
           ismap = 1

       data.append([row['data-pid'], ismap])
           
    return data

def write_data():
    pass

def main():
    
    subdomain = "bham"
    section = "hhh"
    step = 100
    directory = "data/"
    fname_stub = "-".join([subdomain, section, str(step)])
    ext = ".html"

    url = "http://" + subdomain + ".craigslist.org/" + section + "/index" + str(step) + ".html#list"
    fname = directory + fname_stub + ext

    cache_data(url, fname)
    soup = load_data(fname)
    data = parse_data(soup)


if __name__ == "__main__":

    print "welcome"
    print "--------------"
    main()

