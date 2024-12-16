from href_func import *
from details_func import *
from Initialize import initialize
from next import next
from next_batch import next_batch
import csv

#scrape_links_and_next_page("https://www.hltv.org/results")
#data=initialize()
print(next_batch()[0])
#scrape_links_and_next_page(next_batch()[0])
data=next("https://www.hltv.org/matches/2377945/sashi-vs-aurora-young-blud-european-pro-league-season-21")
print(data)
while True:
    data=[f[0] for f in data]
    last=data[-1]
    #print(data)
    #input()
    for d in data:
        #print(d)
        #input()
        scrape_match_data(str(d))
    if input()=="O":
        break
    scrape_links_and_next_page(next_batch()[0])
    data=next(last[0])
