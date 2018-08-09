import pandas as pd
import numpy as np
import json
import csv
from sklearn.decomposition import PCA
import datetime


"""
json data processing methods
"""

def activate(activity_json):
    """

    :return:
    """
    activity_json = str(activity_json)
    if activity_json == 'nan' or 'type' not in activity_json:
        return 'nan'
    i1 = activity_json.find('type')
    activity_json = activity_json[i1:]
    i2 = activity_json.find(',')
    activity_json = activity_json[:i2]
    return activity_json


def replace_tabs(str):
    """

    :param str:
    :return:
    """

    str_split = str.split("type': '")
    type_split = str_split[1].split("'")
    type = type_split[0]
    return type

def process_json():
    with open('LocationHistory.json', 'r') as fh:
        raw = json.loads(fh.read())

    ld = pd.DataFrame(raw['locations'])
    del raw  # free up some memory
    # convert to typical units
    ld['latitudeE7'] = ld['latitudeE7'] / float(1e7)
    ld['longitudeE7'] = ld['longitudeE7'] / float(1e7)
    ld['timestampMs'] = ld['timestampMs'].map(
        lambda x: float(x) / 1000)  # to seconds
    ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)
    # Rename fields based on the conversions we just did
    ld.rename(columns={'latitudeE7': 'latitude', 'longitudeE7': 'longitude',
                       'timestampMs': 'timestamp'}, inplace=True)
    ld = ld[
        ld.accuracy < 1000]  # Ignore locations with accuracy estimates over 1000m
    ld.reset_index(drop=True, inplace=True)
    ld = ld[['latitude', 'longitude', 'datetime', 'activity'] ]
    ld = ld.dropna(subset=['latitude', 'longitude', 'datetime','activity'])
    ld['activity'] = ld['activity'].apply(lambda x: activate(x))
    ld['activity'] = ld['activity'].apply(lambda x : replace_tabs(x))

    ld['weekday'] = ld['datetime'].apply(lambda x : x.weekday())
    ld['hour'] = ld['datetime'].apply(lambda x: x.hour)
    ld = ld.drop(['datetime'], axis=1)
    # # one hot encoding for weekday and activity features
    # weekday = ld['weekday']
    # ld = pd.get_dummies(ld, columns=['weekday'])
    # ld = ld.join(weekday)
    # ld = pd.get_dummies(ld, columns=['activity'])
    #
    # # cyclic encoding for hour-of-day
    # hour_after = ld['hour'].apply( lambda x : x+1)
    # hour_before = ld['hour'].apply( lambda x : x-1)
    # hour_of_day = pd.get_dummies(ld['hour'])
    #
    # hour_after_d = pd.get_dummies(hour_after).apply(lambda x : x*(0.5))
    # hour_before_d = pd.get_dummies(hour_before).apply(lambda x : x*(0.5))
    # hour_after_d = hour_after_d.rename(columns={24: 0})
    # hour_before_d = hour_before_d.rename(columns={-1: 23})
    #
    # for col in hour_before_d.columns:
    #     if col in hour_of_day.columns:
    #         hour_of_day[col] += hour_before_d[col]
    #         del hour_before_d[col]
    #
    # for col in hour_after_d.columns:
    #     if col in hour_of_day.columns:
    #         hour_of_day[col] += hour_after_d[col]
    #         del hour_after_d[col]
    #
    # ld = ld.join(hour_of_day)
    #
    #
    # # lets clean the columns we dont need
    # ld = ld.drop(['hour','datetime'], axis=1)

    # import to csv
    ld.to_csv('history_7_8_18.csv')


def init_keys(places):
    keys = []
    for place1 in places:
        for place2 in places:
            if place1 != place2:
                keys.append(place1+"-"+place2)

    return keys


def get_routes():
    """

    :return:
    """

    # name , weekday , and dummies
    file = open("routes.txt", "r")
    places = []
    keys = init_keys(places)
    # init each route with empty list
    vec_dict = {key: [] for key in keys}
    count_dict = {key: 0 for key in keys}
    current_to, current_weekday_to = ""
    current_from, current_weekday_from = ""
    lines = file.readlines()
    add = False

    for i in range(4000):

        current_to_line = lines[i].split(" ")
        current_to = current_to_line[0]
        current_weekday_to = current_to_line[1]

        if i+1 < len(lines):
            current_from_line = lines[i+1].split(" ")
            current_from = current_from_line[0]
            current_weekday_from = current_from_line[1]

        else:
            print("error!")
            exit(1)

        if current_weekday_from == current_weekday_to and current_from!="":
            vec_dict[current_from+'-'+current_to].appand(list(current_to_line[1:]))
            count_dict[current_from+'-'+current_to] += 1
            add = True

        else:
            add = False

        # mean value of routes

        np_dict = {}

        for key in keys:
            current_np = np.array(vec_dict[key])
            np_dict[key] = np.mean(current_np, axis=1)

        # write to files
        count = csv.writer(open("count.csv", "w"))
        for key, val in count_dict.items():
             count.writerow([key, val])

        vec = csv.writer(open("vec.csv", "w"))
        for key, val in count_dict.items():
             count.writerow([key, np.array2string(val)])




def perform_pca():
    """

    :return:
    """
    data = pd.read_csv("to_pca.csv")
    from_data = pd.get_dummies(data['from_data'])
    to_data = pd.get_dummies(data['to_data'])
    data = data.drop(['from_data','to_data'], axis=1)
    data = data.join(from_data)
    data = data.join(to_data)
    data_to_pca = data.drop(['prec','route'],axis = 1)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data_to_pca)
    principal_df = pd.DataFrame(data=principal_components, columns=['x', 'y'])
    final_df = pd.concat([principal_df, data[
        ['prec', 'route']]], axis=1)
    return final_df



def data_process():

    process_json()

    get_routes()

    map = perform_pca()

    return map















process_json()
