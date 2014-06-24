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

def parse_data(soup):

    content = soup.select("div.content")[0]
    rows = soup.select("p.row")

    data = []

    print "-------------"
    print "found rows: "
    print len(rows)
    print "-------------"

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
    main()

##http://bham.craigslist.org/hhh/index100.html#list



##rows = content[0].select(".row")

#.find_all({'class':'row'})

#soup.select("[class~=sister]")


#.find(class="row")

#for link in soup.find_all('id'):
#    print(link.get('href'))

#{ "class" : "lime" })


#tree = html.fromstring(page.text)

#This will create a list of buyers:
#xpath_string = '//*[@id="toc_rows"]/div[2]/p[1]'

#items = tree.xpath(xpath_string)

#print items

#This will create a list of prices
# prices = tree.xpath('//span[@class="item-price"]/text()')


    
