from osgeo import ogr, osr

class dataset():
    """
    provides some common dataset code.
    """

    def __init__(self):
        self.layers = {}
        self.dataSources = {}

        self.config = {'block': {'driver': 'ESRI Shapefile',
                                 'filename': r'C:\personal\BeeSafeBoulder\data\blocks_sp\blocks.shp'},
                       'parcel': {'driver': 'ESRI Shapefile',
                                  'filename': r'C:\personal\BeeSafeBoulder\data\parcels\Parcels.shp'},
                       'address': {'driver': 'ESRI Shapefile',
                                   'filename': r'C:\personal\BeeSafeBoulder\data\addresses\addresses.shp'},
                       'neighborhood': {'driver': 'ESRI Shapefile',
                                   'filename': r'C:\personal\BeeSafeBoulder\data\BeeSafeNeighborhood\BeeSafeNeighborhood.shp'}}

        for name, info in self.config.iteritems():
            driver = ogr.GetDriverByName(info['driver'])
            dataSource = driver.Open(info['filename'], 1)
            self.dataSources[name] = dataSource

            layer = dataSource.GetLayer()

            self.layers[name] = layer

    # define __enter__ and __exit__ to support the "with" pattern.
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for name, datasource in self.dataSources.iteritems():
            datasource.Destroy()
