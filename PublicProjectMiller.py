#-------------------------------------------------------------------------------
# Name:        ProjectMiller
# Purpose:     Generates Asset mbtiles files from a TileMill map.  Also uploads the mbtiles.
#
# Author:      Alfred
#
# Created:     12/12/2012
#-------------------------------------------------------------------------------
from TileMill import *
import os
import shutil

tilemill_dir = r'C:\Program Files (x86)\TileMill-v0.10.1\tilemill'
projectFilesLocation = r'C:\personal\BeeSafeBoulder\TileMillProjects'

access_account = r'MAPBOX_USERNAME'
access_token = r'MAPBOX_ACCESS_TOKEN'

# remove the cache directory so that we can use the most recent outage information
# from the internet.
cachePath = os.path.join(projectFilesLocation, 'cache')
if os.path.exists(cachePath):
    shutil.rmtree(cachePath)

output_dir = os.path.join(projectFilesLocation, 'output')
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

tm = TileMill(tilemill_dir)


projects = [
    {'projectName': 'BeeSafeBoulderPublic',
     'bbox': '-105.6674,39.9098,-105.0558,40.2608',
     'minzoom': 0,
     'maxzoom': 16}
]

for project in projects:
    name = project['projectName']
    filename = os.path.join(output_dir, '%s.png' % (name))
    tm.render(name, filename,
              format='png',
              bbox=project['bbox'],
              width=400,
              height=400,
              files=projectFilesLocation,
              quiet=False)

    filename = os.path.join(output_dir, '%s.mbtiles' % (name))

    tm.render(name, filename,
              format='mbtiles',
              bbox=project['bbox'],
              minzoom=project['minzoom'],
              maxzoom=project['maxzoom'],
              metatile=2,
              files=projectFilesLocation)

    tm.modify_metadata(filename,
                       {'name': name})

    tm.upload(name, filename, access_account, access_token, files=projectFilesLocation)