import json
import time
import sys

from arcgis.gis import GIS
from arcgis.mapping import MapImageLayer
from arcgis.mapping import WebMap


# get username and password
username = input('ArcGIS Online username: ')
passwd = input('ArcGIS Online password: ')


# connect to my arcgis account (Which happens to be part of IRWIN)
my_gis = GIS('https://www.arcgis.com', username, passwd)
print(my_gis)

# connect to EMEF's map server, get the points and the admin boundaries
ef_points = MapImageLayer('https://geopub.epa.gov/arcgis/rest/services/EMEF/efpoints/MapServer/')
ef_boundaries = MapImageLayer('https://geopub.epa.gov/arcgis/rest/services/EMEF/Boundaries/MapServer/')

superfund_points = ef_points.layers[0]
toxic_releases = ef_points.layers[1]
counties = ef_boundaries.layers[5]
states = ef_boundaries.layers[6]

# we know which layers to add, so create blank webmap to add it to. This one has dark gray canvas
darkGray = my_gis.content.search('title:dark', outside_org=True, item_type='web map')[0]
my_webmap = WebMap(darkGray)

# add the feature layers to the dark gray canvas map
my_webmap.add_layer(counties)
my_webmap.add_layer(states)

my_webmap.add_layer(superfund_points)
my_webmap.add_layer(toxic_releases)

# Set the webmap properties and tags, then save it to my gis. If one already exists with the same name,
# it will create 2

webmap_name = 'my webmap'
webmap_item_properties = {'title': webmap_name,
                         'snippet': webmap_name,
                         'tags':['webmap', 'epa', 'python']}

my_webmap.save(webmap_item_properties)

# to make changes to the initial map, need to share it publically
my_webmap = my_gis.content.search(webmap_name, item_type="Web Map")

# make sure webmap exists first
while len(my_webmap) == 0:
    if len(my_webmap) == 1:
        break

my_webmap = my_webmap[0]
my_webmap.share(everyone=True)

# update extent of webmap- this one is Manhattan
update_parameters = {'extent': '-74.227,40.537,-73.601,40.862'}
my_webmap.update(update_parameters)

# going to update symbology. Open this file, which defines symbology
with open('symb2.json') as json_data:
    data = json.load(json_data)

# create item properties, fill it with the symbology in the file
item_properties = {"text": json.dumps(data)}

# update webmap with those properties from the symbology json file
my_webmap.update(item_properties=item_properties)

webmap_id = my_webmap.id
link = 'https://geoplatform.maps.arcgis.com/home/webmap/viewer.html?webmap={}'.format(webmap_id)

print('copy/paste this link in browser to open the webmap')
print(link)
