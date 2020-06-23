#!/usr/bin/env python
# coding: utf-8

# # Peer-graded Assignment: Segmenting and Clustering Neighborhoods in Toronto
# 

# # PART 1:

# For this assignment, you will be required to explore and cluster the neighborhoods in Toronto.
# 
# 1) Start by creating a new Notebook for this assignment.
# 2) Use the Notebook to build the code to scrape the following Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe like the one shown below:

# In[38]:


import requests
import lxml.html as lh
import pandas as pd


# In[2]:


wikipedia_link='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

#Create a handle, wikipedia_page, to handle the contents of the website
wikipedia_page=requests.get(wikipedia_link)

#Store the contents of the website under wikipedia_page
wikipedia_page = lh.fromstring(wikipedia_page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = wikipedia_page.xpath('//tr')

#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]


# In[3]:


tr_elements = wikipedia_page.xpath('//tr')

#Create empty list
col=[]

i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print(name)
    col.append((name,[]))


# In[4]:


col


# In[5]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[6]:


[len(C) for (title,C) in col]


# In[7]:


# Transforming the dictionary on a dataframe
Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)


# In[8]:


# Cleaning break lines
df = df.replace(r'\n','', regex=True)
df.columns = ['Postcode', 'Borough', 'Neighbourhood']
df.head()


# In[10]:


#Removing Not assigned zip codes and fixing df index
df.drop(df[df['Borough'] == 'Not assigned'].index, inplace=True)
df.index = range(len(df))
df


# In[11]:


df.shape


# 3) To create the above dataframe:
# 
# The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
# Only process the cells that have complete information and not greyed out or not assigned.
# For each cell, the postal code will go under the PostalCode column, the first line under the postal code will go under Borough, and the remaining lines will go under the Neighborhood column formatted nicely and separated with commas as shown in the sample dataframe above. For example, for cell (1, 3) on the Wikipedia page, M3A will go under PostalCode, North York will go under Borough, and Parkwoods will go under Neighborhood.
# If a cell has only one line under the postal code, like cell (1, 7), then that line will go under the Borough and the Neighborhood columns. So for cell (1, 7), the value of the Borough and the Neighborhood column will be Queen's Park.
# Clean your Notebook and add Markdown cells to explain your work and any assumptions you are making.
# In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.
# 
# 
# 4) Submit a link to your Notebook on your Github repository. (10 marks)
# 
# Note: There are different website scraping libraries and packages in Python. One of the most common packages is BeautifulSoup. Here is the package's main documentation page: http://beautiful-soup-4.readthedocs.io/en/latest/
# The package is so popular that there is a plethora of tutorials and examples of how to use it. Here is a very good Youtube video on how to use the BeautifulSoup package: https://www.youtube.com/watch?v=ng2o98k983k
# Use the BeautifulSoup package to transform the data in the table on the Wikipedia page into the above pandas dataframe

# # PART 2:

# Now that you have built a dataframe of the postal code of each neighborhood along with the borough name and neighborhood name, in order to utilize the Foursquare location data, we need to get the latitude and the longitude coordinates of each neighborhood.
# In an older version of this course, we were leveraging the Google Maps Geocoding API to get the latitude and the longitude coordinates of each neighborhood. However, recently Google started charging for their API: http://geoawesomeness.com/developers-up-in-arms-over-google-maps-api-insane-price-hike/, so we will use the Geocoder Python package instead: https://geocoder.readthedocs.io/index.html.
# The problem with this Package is you have to be persistent sometimes in order to get the geographical coordinates of a given postal code. So you can make a call to get the latitude and longitude coordinates of a given postal code and the result would be None, and then make the call again and you would get the coordinates. So, in order to make sure that you get the coordinates for all of our neighborhoods, you can run a while loop for each postal code. Taking postal code M5G as an example, your code would look something like this:
# # initialize your variable to None
# lat_lng_coords = None
# 
# # loop until you get the coordinates
# while(lat_lng_coords is None):
#   g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
#   lat_lng_coords = g.latlng
# 
# latitude = lat_lng_coords[0]
# longitude = lat_lng_coords[1]
# 
# Use the Geocoder package to get the latitude and the longitude coordinates for all the neighborhoods in our dataframe. Here is a sample of the resulting dataframe for your reference.

# In[12]:


#!conda install -c conda-forge geocoder --yes
import geocoderimport pandas as pd

import numpy as np


# In[13]:


# initialize your variable to None
lat_lng_coords = None

#Create extra columns
df['Latitude'] = pd.Series("", index=df.index)
df['Longitude'] = pd.Series("", index=df.index)

df.columns


# In[ ]:


# loop until you get the coordinates
i = 0

sum_latitude = sum(df['Latitude'] == '')

while sum_latitude > 0:
    print('Missing coordinates: '+sum_latitude) 
    if df['Latitude'][i] == '':
        try:
            g = geocoder.google('{}, Toronto, Ontario'.format(df['Neighbourhood'][i]))
            lat_lng_coords = g.latlng
            if g.latlng != None:
                df['Latitude'][i] = lat_lng_coords[0]
                df['Longitude'][i] = lat_lng_coords[1]
        except:
            break
    i = i+1
    sum_latitude = sum(df['Latitude'] == '')


df


# # PART 3:

# Explore and cluster the neighborhoods in Toronto. You can decide to work with only boroughs that contain the word Toronto and then replicate the same analysis we did to the New York City data. It is up to you.
# Just make sure:   
# 
#     
#     - to add enough Markdown cells to explain what you decided to do and to report any observations you make.
#     - to generate maps to visualize your neighborhoods and how they cluster together.
#     
# Once you are happy with your analysis, submit a link to the new Notebook on your Github repository. (3 marks)

# In[ ]:


#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim 

#Use geopy library to get the latitude and longitude values of Toronto
address = 'Toronto,ON'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of ',address,' are {}, {}.'.format(latitude, longitude))


# In[ ]:


#!conda install -c conda-forge folium=0.5.0 --yes 
import folium # map rendering library

# create map of Toronto using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighbourhood in zip(df['Latitude'], df['Longitude'], df['Borough'], df['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
            
map_toronto

