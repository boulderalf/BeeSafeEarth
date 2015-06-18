from osgeo import ogr
import gspread # pip install gspread
import os
import json
from pprint import pprint
from dataset import dataset
import winsound
from credentials import Credentials


# updates pledge spreadsheet with ASR_ID and Normalized Address
# updates parcels with pledge level
# updates addresses with pledge level

# see http://gspread.readthedocs.org/en/latest/oauth2.html

with dataset() as ds:

    gc = gspread.authorize(Credentials())
    sht = gc.open("BeeSafe Pledge (Responses)").worksheet("Form Responses 1")

    # call get_all_values() to get the header and
    values = sht.get_all_values()

    # first, create a column header lookup
    header_column = {}

    for column, header in enumerate(values[0]):
        header_column[header] = column + 1

    print header_column

    def data(row):
        data = {}

        for header, column in header_column.iteritems():
            data[header] = None if column > len(row) else row[column-1]

        return data

    updated_cells = []

    def update_cell(sht, col_number, row_number, value):
        c = sht.cell(row_number, col_number)
        c.value = value
        updated_cells.append(c)

    def update_feature(addressLayer, addressFeature, parcelLayer, sht, row_number, data_row):
        col_number = header_column['Normalized Street Address']
        value =  "{}, {}, {}".format(addressFeature.GetField('ADDRESS'),
                                     addressFeature.GetField('CITY'),
                                     addressFeature.GetField('STATE'))
        update_cell(sht, col_number, row_number, value)

        col_number = header_column['ASR_ID']
        value = addressFeature.GetField('ASR_ID')
        update_cell(sht, col_number, row_number, value)

        addressFeature.SetField('PLEDGE', 'YES')
        if data_row['May we show your pledge on a public map?'] is not None and data_row['May we show your pledge on a public map?'].lower() == 'yes':
            addressFeature.SetField('SHOW_ON_MA', 1)
        addressLayer.SetFeature(addressFeature)

        parcelLayer.SetAttributeFilter('ASR_ID = "{}"'.format(addressFeature.GetField('ASR_ID')))
        parcels = list(parcelLayer)

        if len(parcels) > 0:
            parcelFeature = parcels[0]
            parcelFeature.SetField('PLEDGE', 'YES')
            if data_row['May we show your pledge on a public map?'] is not None and data_row['May we show your pledge on a public map?'].lower() == 'yes':
                parcelFeature.SetField('SHOW_ON_MA', 1)
            parcelLayer.SetFeature(parcelFeature)

    addressLayer = ds.layers['address']
    parcelLayer = ds.layers['parcel']

    for idx, r in enumerate(values[1:]):
        if len(updated_cells) >= 10:
            print updated_cells
            sht.update_cells(updated_cells)
            del updated_cells[:]

        row_number = idx + 2
        row = data(r)
        print row_number, row

        if len(row['Normalized Street Address'].strip()) > 0:
            # if we have a normalized street address then we can assume that this row has been
            # updated by this script.  Continue to the next row.
            continue

        entered_street_address = row['Street Address']

        matches = []
        # first, try a strict match
        matches.append(entered_street_address.upper().strip().replace('.', ''))
        # then try a match on first two elements
        matches.append(" ".join([x for x in entered_street_address.upper().strip().replace(',', '').replace('.', '').split(' ') if x][0:2]))
        # finally try a match on first element only
        matches.append(" ".join([x for x in entered_street_address.upper().strip().replace(',', '').replace('.', '').split(' ') if x][0:1]))

        for match in matches:
            print "match: {} ".format(match)
            addressLayer.SetAttributeFilter('(ADDR_FMT = "EXACT") AND (ADDRESS like "{} %")'.format(match))
            addressFeatures = list(addressLayer)

            # pledgeLevel = d['Pledge Level'].split(' ')[-1]
            # print "pledgeLevel {}".format(pledgeLevel)
            if len(addressFeatures) == 1:
                print "For entered address '{}' we have found the following single match:".format(entered_street_address)
                addressFeature = addressFeatures[0]
                print "\t'{}, {}, {}' (ASR_ID={})\n".format(addressFeature.GetField('ADDRESS'),
                                                                addressFeature.GetField('CITY'),
                                                                addressFeature.GetField('STATE'),
                                                                addressFeature.GetField('ASR_ID'))
                update_feature(addressLayer, addressFeature, parcelLayer, sht, row_number, row)
                break

            if len(addressFeatures) == 0:
                #update_cell(sht, header_column['Normalized Street Address'], row_number, entered_street_address)
                print "\tskipping because we found no matches"
                continue

            # if we do not find a strict match, the do it based on address number and prompt the user for feedback
            print "For entered address '{}' we have found the following matches:".format(entered_street_address)

            addressList = []
            for address in addressFeatures:
                addressList.append(address)

            skip = "SKIP"
            less_strict = "LESS STRICT"

            addressList = sorted(addressList, key = lambda a: a.GetField('ADDRESS'))
            addressList.append(skip)
            addressList.append(less_strict)

            for idx, address in enumerate(addressList):
                if str(address) == skip:
                    print "\t{}) {}".format(idx, skip)
                elif str(address) == less_strict:
                    print "\t{}) {}".format(idx, less_strict)
                else:
                    print "\t{}) {}, {}, {} (ASR_ID={})".format(idx, address.GetField('ADDRESS'),
                                                                address.GetField('CITY'),
                                                                address.GetField('STATE'),
                                                                address.GetField('ASR_ID'))

            winsound.Beep(1000,1000)
            id = int(raw_input("Enter # of matching address > "))

            addressFeature = addressList[id]

            if str(addressFeature) == less_strict:
                continue

            elif str(addressFeature) == skip:
                sht.update_cell(row_number, header_column['Normalized Street Address'], skip)
                sht.update_cell(row_number, header_column['ASR_ID'], skip)
                break
            else:
                print "you chose '{}, {}, {}' (ASR_ID={})\n".format(addressFeature.GetField('ADDRESS'),
                                                          addressFeature.GetField('CITY'),
                                                          addressFeature.GetField('STATE'),
                                                          addressFeature.GetField('ASR_ID'))

                update_feature(addressLayer, addressFeature, parcelLayer, sht, row_number, row)
                break

    print updated_cells
    sht.update_cells(updated_cells)