## To Install ESRI Python API

Taking one of the paths from the instructions here: https://developers.arcgis.com/python/guide/install-and-set-up/


1. Install Conda

2. Create a Python 3 environment (or not, if you already are using Python 3.x)

3. From the Python 3 environment:

    `conda install -c esri arcgis`

4. Test that it worked:
    <br/>`from arcgis.gis import GIS`
    <br/>`my_gis = GIS()`
    <br/>`m = my_gis.map()`
    <br/>`m`
    
    
## To run this code
From inside the Python3 environment, 
`create_webmap.py`

enter ArcGIS Online credentials when prompted

after the code completed, go to your content and find the web map

Running the html code:
-  python3 -m http.server
