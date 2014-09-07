# TileMill

This product contains code for automating TileMill rendering and export.  It requires that you have [TileMill](http://mapbox.com/tilemill/) installed on your computer.

The Python wrapper currently supports rendering a project with `render()`, updating an MBTile file's metadata with `modify_metadata()` and uploading an MBTile file to [MapBox](http://mapbox.com) if you have an account with `upload()`.

Example of rendering a project to PNG file.

~~~python
from TileMill import *

tilemill_dir = r'C:\Program Files (x86)\TileMill-v0.10.1\tilemill'
tm = TileMill(tilemill_dir)

tilemill_project_name = 'SLO'
tm.render(tilemill_project_name,r'c:\temp\SLO.png',
          format='png',
          width=400,
          height=400)
~~~

You can review the code in `iFactorSandbox\python\SLOmap\SLOProjectMiller.py` for an example of rendering to MBTile format and then uploading to a MapBox account.