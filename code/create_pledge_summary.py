import gspread # easy_install gspread
import os
from dataset import dataset
import csv

email = 'GOOGLE_EMAIL_ADDRESS'
password = 'GOOGLE_PASSWORD'

sht = gspread.login(email, password).open("BeeSafe Pledge (Responses)").worksheet("Form Responses 1")

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

asr_id_rows = {}

for idx, r in enumerate(values[1:]):
    row_number = idx + 2
    row = data(r)
    asr_id_rows[row['ASR_ID']] = row

# creates a CSV file with all pledges in the neighborhood boundary.
with dataset() as ds:
    addressLayer = ds.layers['address']
    neighborhoodLayer = ds.layers['neighborhood']

    for neighborhood in neighborhoodLayer:

        neighborhoodName = neighborhood.GetField("name")

        print neighborhoodName

        targetDir = os.path.join(r'C:\personal\BeeSafeBoulder\GoogleDrive-BeeSafe\BeeSafe', neighborhoodName)
        if not os.path.exists(targetDir):
            os.mkdir(targetDir)

        addressLayer.SetSpatialFilter(neighborhood.GetGeometryRef())
        addressLayer.SetAttributeFilter('ADDR_FMT = "EXACT"')

        addressList = []

        for address in addressLayer:
            addressList.append(address)

        addressList = sorted(addressList, key=lambda a: "{} {}".format(" ".join(a.GetField('ADDRESS').split(' ')[1:]), a.GetField('ADDRESS').split(' ')[0]))

        filename = os.path.join(targetDir,"PrivatePledgeSummary.csv")

        fieldnames = ['Name', 'Address', 'Email', 'Pledge', 'Comments']
        with open(filename, 'wb') as outStream:
            writer = csv.DictWriter(outStream, delimiter=',', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))

            for address in addressList:
                asr_id = address.GetField('asr_id')

                if asr_id in asr_id_rows:
                    row = asr_id_rows[asr_id]

                    writer.writerow({'Name':     row['Name'],
                                     'Address':  row['Normalized Street Address'],
                                     'Email':    row['Email Address'],
                                     'Pledge':   row['Pledge Level'],
                                     'Comments': row['Comments']})
