import requests
import json


def get_census_data(route, filename):
    """Get data from a route and return as a JSON file.

        This is meant to be used with the Census Data API to save
        data locally in my preferred format:

        ['AREA NAME' (str), people (int), state id (int), district id (int)]
    """
    # save data from API route as local variable & format as json

    data = requests.get(route)
    json_data = data.json()

    # change numeric data into integers

    for i in range(1, len(json_data)):
        for j in range(1, len(json_data[i])):
            json_data[i][j] = int(json_data[i][j])

    # save json data as file in project folder

    proj_folder = '/home/vagrant/src/Project/data'

    with open('%s/%s' % (proj_folder, filename), 'w') as outfile:
        json.dump(json_data, outfile)
