import csv

with file('location.csv', 'rb') as f:
   reader = csv.reader(f)
   location_list = list(reader)

for item in location_list:
    loc = Location(location_id=item[0], district_id=item[1], state_name='item[2]')
