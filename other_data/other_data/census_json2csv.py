import json
import csv

CSV_FILENAMES = ['allmale_census2015.csv',
                 'allfemale_census2015.csv',
                 'mngmt_male_census2015.csv',
                 'mngmt_female_census2015.csv']

JSON_FILENAMES = ['allmale_census2015.json',
                  'allfemale_census2015.json',
                  'mngmt_male_census2015.json',
                  'mngmt_female_census2015.json']

    jfile = open(JSON_FILENAME)
    jfile = json.load(jfile)
    for item in jfile:
        del item[0]

    with open(CSV_FILENAME, 'wb') as cfile:
        writer = csv.writer(cfile)
        writer.writerows(jfile)
