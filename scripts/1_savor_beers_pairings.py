from requests import get
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.savorcraftbeer.com/experience/food-pairings/'
container_type = 'container'

response = get(URL, verify = False)
#print(response.text[:500])

html_soup = BeautifulSoup(response.text, 'html.parser')
#print(html_soup)

containers = html_soup.find_all('div', container_type)  #beers and brewery lists are stored in flex containers
#print(containers[0])  #print first one to get a sample of the html
#print(containers[0].h4.text)  ##location of brewery
#print(containers[0].li)

planning = str(containers[0].h4).replace('>','_').replace('<','_').split('_')
print(planning)


brewery_name = []
brewery_location = []
beer_name = []
food = []

for container in containers:
    brewery = (str(container.h4).replace('>','_').replace('<','_').replace('&amp;','&').split('_'))[2]
    brewery_name.append(brewery) #add brewery to list
    loc = str(container.find('div').text).strip()
    brewery_location.append(loc)

pairing_df = pd.DataFrame({
    'brewery': brewery_name,
    'location': brewery_location
})

total_df = pd.merge(pairing_df, beer_df, how = 'left', on='brewery') #add location to the beer df

total_df.to_csv('path/to/file/beers.csv', header = True, index = False)
