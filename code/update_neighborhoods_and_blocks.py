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
    blockLayer = ds.layers['block']
    addressLayer = ds.layers['address']

    for layer in [neighborhoodLayer, blockLayer]:
        for feature in layer:
            addressLayer.SetSpatialFilter(feature.GetGeometryRef())
            addressLayer.SetAttributeFilter(None)
            total = len(list(addressLayer))
            feature.SetField('add_total', total)

            addressLayer.SetSpatialFilter(feature.GetGeometryRef())
            addressLayer.SetAttributeFilter('PLEDGE = "YES"')
            yes = len(list(addressLayer))
            feature.SetField('add_yes', yes)
            feature.SetField('not_yes', total - yes)

            addressLayer.SetSpatialFilter(feature.GetGeometryRef())
            addressLayer.SetAttributeFilter('PLEDGE = "NO"')
            feature.SetField('add_no', len(list(addressLayer)))

            layer.SetFeature(feature)
