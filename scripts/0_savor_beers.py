from requests import get
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.savorcraftbeer.com/experience/beers/'
container_type = 'flex-container'

response = get(URL, verify = False)
#print(response.text[:500])

html_soup = BeautifulSoup(response.text, 'html.parser')
#print(html_soup)

containers = html_soup.find_all('div', container_type)  #beers and brewery lists are stored in flex containers
#print(containers[0])  #print first one to get a sample of the html
#print(containers[0].h4.text)  ##location of brewery
#print(containers[0].li)


brewery_name = []
beer_name = []
beer_style = []
beer_abv = []

for container in containers:
    brewery = container.h4.text
    brewery_name.append(brewery) #add brewery to list
    brewery_name.append(brewery) #add again because there's two beers per
    beer_details = container.find_all('span', class_ = 'beer-details')
    for beer in beer_details:
        new_beer = str(beer)
        clean_beer = new_beer.replace('>', '_').replace('<', '_')
        new_clean_beer = clean_beer.split('_')
        beer_name.append(new_clean_beer[2])
        beer_abv.append(new_clean_beer[4].replace('% ABV',''))
        beer_style.append(new_clean_beer[-5].replace('(','').replace(')',''))

##this is awful - should just make a df with a row per beer here

beer_df = pd.DataFrame({
    'brewery': brewery_name,
    'beer': beer_name,
    'style': beer_style,
    'abv': beer_abv
})

beer_df.head(200)
beer_df.info()

beer_df.to_csv('/Users/jzavilla/Documents/Personal/python/beers.csv', header = True)
