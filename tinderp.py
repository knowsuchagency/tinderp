from __future__ import print_function
from pprint import pprint
from pymongo import MongoClient
import logging
import pynder

def normalize(user, wanted_attributes=None):
    """
    Convert a User object to a dictionary based on the wanted attributes.
    Return None if User can't be marshalled into a dictionary.
    """
    wanted_attributes = wanted_attributes or ['name',
                                              'id',
                                              'instagram_username',
                                              'age',
                                              'distance_km',
                                              'bio',
                                              'photos']
    # skip profiles without names
    if getattr(user, 'name', None) is None:
        return None

    dictionary = {}
    for attr in wanted_attributes:
        try:
            key, value = attr, getattr(user, attr, None)
            # rename 'id' to '_id' so that it becomes the index in mongodb
            if key == 'id': key = '_id'
        except Exception as e:
            logging.warning(e)
        dictionary[key] = value

    return dictionary

client = MongoClient()
db = client.tinderp
session = pynder.Session("1165230333",
                         "CAAGm0PX4ZCpsBAHXfAZBKUuVbihBK87NKPegNZB9ypmIvbaxCSGc6ZB6BmMSeUTEujO0vCjJkq9kVCy1IZB9GPVlQZCAtvzAN5AOHDpZBWQRL0e1VnOqYuK9yZAh11i8TpX5l94PmjsrXBcJeJw9z9SZCAsn41RaqpwJ5iKOKXkyBsZCFL3v13VkF42P575DN26NNrHPgVxfYMC4CLIsVDifbE")

wanted_attributes = ['name',
                     'id',
                     'instagram_username',
                     'age',
                     'distance_km',
                     'bio',
                     'photos']

match_collection = db.matches
matches = session.matches()
normalized_matches = []
print()
for match in matches:
    d = {}
    for attr in wanted_attributes:
        try:
            key, value = attr, getattr(match.user, attr, None)
            if key == 'id': key = '_id'
        except Exception as e:
            logging.warning(e)
        d[key] = value
    if d['name'] is not None:
        normalized_matches.append(d)


print('\n' * 4)
pprint(normalized_matches)
[match_collection.replace_one({'_id': match['_id']}, match, upsert=True) for match in normalized_matches]
