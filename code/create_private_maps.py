from osgeo import ogr, osr
from stringtemplate3 import StringTemplate, StringTemplateGroup # easy_install stringtemplate3
import gspread # easy_install gspread
import os
import json
import subprocess
from TileMill import *
from dataset import dataset
import urllib


with dataset() as ds:
    neighborhoodLayer = ds.layers['neighborhood']

    tilemill_dir = r'C:\Program Files (x86)\TileMill-v0.10.1\tilemill'
    projectFilesLocation = r'C:\personal\BeeSafeBoulder\TileMillProjects'

    output_dir = r'C:\personal\BeeSafeBoulder\temp'

    tm = TileMill(tilemill_dir)
    name = "BeeSafeBoulderPrivate"
    filename = os.path.join(output_dir, 'PrivateMap.png')

    llSRS = osr.SpatialReference()
    llSRS.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(neighborhoodLayer.GetSpatialRef(), llSRS)

    def get_neighborhood_for_block(block):
        """
        gets the related neighborhood for BLOCK
        """
        layer = ds.layers['neighborhood']
        layer.SetSpatialFilter(block.GetGeometryRef().Centroid())

        for neighborhood in layer:
            return neighborhood

    for neighborhood in neighborhoodLayer:

        neighborhoodName = neighborhood.GetField("name")

        print neighborhoodName

        geom = neighborhood.GetGeometryRef().Clone()
        geom.Transform(transform)

        bbox = '{0},{2},{1},{3}'.format(*geom.GetEnvelope())

        tm.render(name, filename,
                  format='png',
                  bbox=bbox,
                  width=1300,
                  height=1200,
                  files=projectFilesLocation)

        targetDir = os.path.join(r'C:\personal\BeeSafeBoulder\GoogleDrive-BeeSafe\BeeSafe', neighborhoodName)
        if not os.path.exists(targetDir):
            os.mkdir(targetDir)

        newFilename = os.path.join(targetDir, os.path.basename(filename))

        if os.path.exists(newFilename):
            os.unlink(newFilename)

        os.rename(filename,newFilename)
