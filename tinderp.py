from __future__ import print_function
import logging
import pynder

def get_matches(session):
    """
    Return a list of user dictionaries from matches.
    """

    matches = [m.user.dict() for m in session.matches(filter_empty_matches=True)]
    matches["_id"] = matches.pop("id")

def get_hopefuls(session, limit=10, verbose=False):
    """
    Return a list of user dictionaries from hopefuls.

    Likes them on the way in :)
    """
    result = []
    hopefuls = session.nearby_users(limit=limit)
    for hopeful in hopefuls:
        hopeful.like()

    if verbose:
        for hopeful in hopefuls:
            try:
                print("Just liked:", hopeful)
            except UnicodeEncodeError as e:
                hopeful = unicode(hopeful.__str__(), errors='ignore')
                print("Just liked:", hopeful)


    for hopeful in hopefuls:
        d = hopeful.dict()
        d["_id"] = d.pop("id")
        result.append(d)
    return result


def persist(collection, user):
    collection.replace_one({"_id": user["_id"]}, user, upsert=True)

if __name__ == "__main__":
    from pprint import pprint
    from pymongo import MongoClient
    from six.moves import configparser
    import os

    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.api_tokens.conf"))
    user_id = config.get("tinder", "id")
    token = config.get("tinder", "token")

    session = pynder.Session(user_id, token)
    client = MongoClient()
    db = client.tinderp
    match_collection = db.matches
    hopefuls_collection = db.hopefuls

    hopefuls = get_hopefuls(session, limit=100, verbose=True)
    while hopefuls:
        print("liked {} people".format(len(hopefuls)))
        for hopeful in hopefuls:
            persist(hopefuls_collection, hopeful)

        hopefuls = get_hopefuls(session, limit=100, verbose=True)
