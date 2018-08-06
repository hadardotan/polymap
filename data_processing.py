import pandas as pd
import json
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

    # one hot encoding for weekday and activity features
    ld = pd.get_dummies(ld, columns=['weekday'])
    ld = pd.get_dummies(ld, columns=['activity'])

    # cyclic encoding for hour-of-day
    hour_after = ld['hour'].apply( lambda x : x+1)
    hour_before = ld['hour'].apply( lambda x : x-1)
    hour_of_day = pd.get_dummies(ld['hour'])

    hour_after_d = pd.get_dummies(hour_after).apply(lambda x : x*(0.5))
    hour_before_d = pd.get_dummies(hour_before).apply(lambda x : x*(0.5))
    hour_after_d = hour_after_d.rename(columns={24: 0})
    hour_before_d = hour_before_d.rename(columns={-1: 23})

    for col in hour_before_d.columns:
        if col in hour_of_day.columns:
            hour_of_day[col] += hour_before_d[col]
            del hour_before_d[col]

    for col in hour_after_d.columns:
        if col in hour_of_day.columns:
            hour_of_day[col] += hour_after_d[col]
            del hour_after_d[col]

    ld = ld.join(hour_of_day)


    # lets clean the columns we dont need
    ld = ld.drop(['hour','datetime'], axis=1)




    ld.to_csv('history_6_8_18.csv')




process_json()