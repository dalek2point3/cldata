import threetaps
import datetime

client = threetaps.Threetaps('90f9fba463854699328750202c517bb1')


params = {'location.city': 'USA-NYM-NEY', 'source':'CRAIG', 'category' : 'SFUR', 'timestamp' : '2012-02-01..2012-02-03', 'retvals' : ['id,source,heading,price,timestamp,location']}

# params = {'location.city': 'USA-NYM-NEY', 'source':'CRAIG', 'category' : 'SFUR'}

items = client.search.search(params)

print "hi"
for posting in items['postings']:
    print posting['heading']
    print posting['id']
    print posting['source']
    print posting['price']
    print posting['location']['formatted_address']
    print(datetime.datetime.fromtimestamp(int(posting['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'))
    print "-------"
    break
