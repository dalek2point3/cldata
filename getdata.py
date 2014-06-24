import requests
from bs4 import BeautifulSoup

def cache_data(url, fname):
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

    print "-------------"
    print "found rows: "
    print len(rows)

    for row in rows:
       ismap = 0
       if len(row.select(".maptag")) == 0:
           ismap = 1
       print row['data-pid'], ismap

def write_data():
    pass

def main():
    
    url = "http://bham.craigslist.org/hhh/index200.html#list"
    fname = "text.html"
    # cache_data(url, fname)
    soup = load_data(fname)
    parse_data(soup)

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


    
