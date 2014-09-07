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
    addressLayer = ds.layers['address']
    blockLayer = ds.layers['block']


    stg = StringTemplateGroup('rows', os.path.join('..', 'canvass-packages', 'st_templates'))

    tilemill_dir = r'C:\Program Files (x86)\TileMill-v0.10.1\tilemill'
    projectFilesLocation = r'C:\personal\BeeSafeBoulder\TileMillProjects'

    output_dir = r'C:\personal\BeeSafeBoulder\canvass-packages'

    tm = TileMill(tilemill_dir)
    name = "BeeSafeBoulderCanvass"
    filename = os.path.join(output_dir, '%s.png' % name)

    llSRS = osr.SpatialReference()
    llSRS.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(blockLayer.GetSpatialRef(), llSRS)

    def get_neighborhood_for_block(block):
        """
        gets the related neighborhood for BLOCK
        """
        layer = ds.layers['neighborhood']
        layer.SetSpatialFilter(block.GetGeometryRef().Centroid())

        for neighborhood in layer:
            return neighborhood

    for block in blockLayer:

        blockName = block.GetField('Name')

        neighborhoodName = get_neighborhood_for_block(block).GetField("name")

        print blockName, neighborhoodName

        geom = block.GetGeometryRef().Clone()
        geom.Transform(transform)

        bbox = '{0},{2},{1},{3}'.format(*geom.GetEnvelope())

        tm.render(name, filename,
                  format='png',
                  bbox=bbox,
                  width=400,
                  height=400,
                  files=projectFilesLocation)

        addressLayer.SetSpatialFilter(block.GetGeometryRef())
        addressLayer.SetAttributeFilter('ADDR_FMT = "EXACT"')

        addressList = []

        for address in addressLayer:
            addressList.append(address)

        addressList = sorted(addressList, key=lambda a: "{} {}".format(" ".join(a.GetField('ADDRESS').split(' ')[1:]), a.GetField('ADDRESS').split(' ')[0]))

        package = stg.getInstanceOf('package')

        package.setAttribute('block', blockName)
        package.setAttribute('captain', block.GetField("Captain"))
        package.setAttribute('neighborhood', neighborhoodName)
        package.setAttribute('image_path', filename)

        count = 0
        row_page = stg.getInstanceOf('row_page')
        package.setAttribute('row_page', row_page)
        firstPageRows = 3
        subsequentPageRows = 7
        rowsPerPage = firstPageRows

        for address in addressList:
            count += 1

            if (count % rowsPerPage) == 0:
                # create a new row_page
                row_page = stg.getInstanceOf('row_page')
                package.setAttribute('row_page', row_page)
                count = 0
                rowsPerPage = subsequentPageRows

            row = stg.getInstanceOf('row')
            row.setAttribute('address', address.GetField('address'))
            row.setAttribute('is_pledged', 'true' if address.GetField("pledge") is not None else None)

            form_address = "{}, {}, {}".format(address.GetField('address'), address.GetField('city'),
                                                address.GetField('state'))

            print form_address

            row.setAttribute('form_address', urllib.quote_plus(form_address))
            row.setAttribute('asr_id', address.GetField('asr_id'))
            row_page.setAttribute('row', str(row))

        htmlFileName = os.path.join('..', 'canvass-packages', 'package-{}.html'.format(blockName))
        pdfFileName = os.path.join('..', 'canvass-packages', 'package-{}.pdf'.format(blockName))

        with open(htmlFileName, 'wb') as o:
            o.write(str(package))

        subprocess.call(["phantomjs", "rasterize.js", htmlFileName, pdfFileName, "11in*8.5in"])
        # if os.path.exists(htmlFileName):
        #     os.unlink(htmlFileName)

        if os.path.exists(filename):
            os.unlink(filename)

        targetDir = os.path.join(r'C:\personal\BeeSafeBoulder\GoogleDrive-BeeSafe\BeeSafe', neighborhoodName)
        if not os.path.exists(targetDir):
            os.mkdir(targetDir)

        newPdfFileName = os.path.join(targetDir, os.path.basename(pdfFileName))

        if os.path.exists(newPdfFileName):
            os.unlink(newPdfFileName)

        os.rename(pdfFileName,newPdfFileName)
