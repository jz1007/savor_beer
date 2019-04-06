from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd

#grab urls to scrape from csv
urls_df = pd.read_csv('<csv>', usecols = ['<colname>'])
urls = urls_df.url.tolist()  #url list should be the actual beer's page
## sample urls #urls = ['https://untappd.com/b/boston-beer-company-samuel-adams-black-harbor-stout/885012/','https://untappd.com/b/cigar-city-brewing-across-the-alley/3000068','https://untappd.com/b/perennial-artisan-ales-abraxas/77322']  ##add the list of URLs from excel file

untappd_url = []
rating = []
num_ratings = []
date_added = []
description = []
ibu = []

count = 0

for url in urls:

    #count iteration
    count += 1
    print('Loading beer '+str(count)+' of '+str(len(urls)))

    response = get(url, verify = True, headers = {'User-agent': 'your bot 0.1'})  #needs useragent string to avoid 429 response
    html_soup = BeautifulSoup(response.text, 'html.parser')
    sleep(randint(2,5))  #so that requests don't get blocked... mimics human behavior

    #html parse
    rate = str(html_soup.find('span', class_ = 'num').text).replace('(','').replace(')','').strip()  #rating score
    num_rate = int(str(html_soup.find('p', class_ = 'raters').text).replace(' Ratings','').replace(',','').replace(' Rating','').strip())  #number of ratings
    date = str(html_soup.find('p', class_ = 'date').text).replace('Added ','').strip() #date added to untapped
    beer_description = str(html_soup.find('div', class_ = 'beer-descrption-read-less').text).replace(' Show Less','').strip()   #long description of beer
    beer_ibu = int(str(html_soup.find('p', class_ = 'ibu').text).replace(' IBU','').replace('No','0').strip())

    #add to lists
    untappd_url.append(url)
    rating.append(rate)
    num_ratings.append(num_rate)
    date_added.append(date)
    description.append(beer_description)
    ibu.append(beer_ibu)

    print('Complete.'

untappd_df = pd.DataFrame({
    'rating': rating,
    'num_ratings': num_ratings,
    'untappd_url': untappd_url,
    'date_added': date_added,
    'description': description,
    'ibu': ibu
})
