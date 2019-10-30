import json
import sys

from arcgis.gis import GIS
from arcgis.mapping import MapImageLayer
from arcgis.mapping import WebMap
import getpass


def fix_answer(answer, map, webmap_name):
    print('Error: input needs to be y or n')
    to_delete = input('"{}" webmap exists, delete it? (y/n): '.format(webmap_name))
    delete_map(to_delete, map, webmap_name)


def delete_map(answer, map, webmap_name):
    if answer == 'y':
        map.delete()
    elif answer == 'n':
        pass
    else:
        fix_answer(answer, map, webmap_name)


# get username and password
username = input('ArcGIS Online username: ')
passwd = getpass.getpass(prompt='ArcGIS Online password: ', stream=None)

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

# give webmap a name (can be changed to user-input prompt)
webmap_name = 'my webmap'

# search for existing webmap, delete if necessary
existing_webmap = my_gis.content.search(webmap_name, item_type="Web Map")
if len(existing_webmap) > 0:
    answer = input('"{}" webmap exists, delete it? (y/n): '.format(webmap_name))
    for i in existing_webmap:
        delete_map(answer, i, webmap_name)

# Set the webmap properties and tags, then save it to my gis. If one already exists with the same name,
# it will create another one
webmap_item_properties = {'title': webmap_name,
                         'snippet': webmap_name,
                         'tags':['webmap', 'epa', 'python']}

print('saving webmap')
my_webmap.save(webmap_item_properties)

# wait until webmap exists before doing anything with it
my_webmap = my_gis.content.search(webmap_name, item_type="Web Map")

while len(my_webmap) == 0:
    my_webmap = my_gis.content.search(webmap_name, item_type="Web Map")
    if len(my_webmap) == 1:
        break

# to make changes to the initial map, need to share it publicly
my_webmap = my_webmap[0]
my_webmap.share(everyone=True)

# update extent of webmap- this one is Manhattan
update_parameters = {'extent': '-74.227,40.537,-73.601,40.862'}
my_webmap.update(update_parameters)

# update symbology to make counties and states no fill, colored outline.
# Open this file, which defines that symbology
with open('symb2.json') as json_data:
    data = json.load(json_data)

# create item properties, fill it with the symbology in the file
item_properties = {"text": json.dumps(data)}

# update webmap with those properties from the symbology json file
my_webmap.update(item_properties=item_properties)

webmap_id = my_webmap.id
link = 'https://geoplatform.maps.arcgis.com/home/webmap/viewer.html?webmap={}'.format(webmap_id)

print('copy/paste this link in browser to open the webmap \n {}'.format(link))
