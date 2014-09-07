#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Alfred
#
# Created:     12/12/2012
# Copyright:   (c) Alfred 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import os
import sqlite3


class TileMill():
    """ provides wrappers around some TileMill -export commands
    """

    def __init__(self, tilemill_dir):
        """ tilemill_dir : directory that contains
        """
        self.__tilemill_dir = tilemill_dir

    def __run_export(self, args):
        """ runs TileMill's "index.js export" command line
        """

        full_args = ['node.exe', 'index.js', 'export']
        full_args.extend(args)
        print " ".join(full_args)


        print subprocess.call(full_args, shell=True, cwd=self.__tilemill_dir)

    def render(self, project_name, output_file_name, **kwargs):
        """ **kwargs are the same as defined in the help for "index.js export"
        """
        args = [project_name, output_file_name]

        job_file_name = os.path.splitext(output_file_name)[0] + ".export"

        for key in kwargs:
            args.append("--%s=%s" % (key, str(kwargs[key])))

        args.append("--log")
        if os.path.exists(job_file_name):
            args.append("--job=%s" % (job_file_name))

        self.__run_export(args)


    def upload(self, mapbox_map_id, mbtiles_file_name, sync_account, sync_access_token, files=None):

        args = [mapbox_map_id,
                mbtiles_file_name,
                '--format=upload',
                '--syncAccount=%s' % sync_account,
                '--syncAccessToken=%s' % sync_access_token]

        if files is not None:
            args.append('--files={}'.format(files))

        self.__run_export(args)

    def modify_metadata(self, mbtiles_file_name, data):
        ''' modifies metadata in mbtiles_file_name based on values in DATA dict
        '''
        conn = sqlite3.connect(mbtiles_file_name)
        c = conn.cursor()

        try:
            for k in data:
                c.execute('REPLACE INTO metadata (name, value) VALUES (?, ?)', (k, data[k]))

            conn.commit()
        finally:
            c.close()
            conn.close()
