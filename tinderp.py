from __future__ import print_function
import logging
import pynder

def get_matches(session):
    """
    Return a list of user dictionaries from matches.
    """

    matches = [m.user.dict() for m in session.matches(filter_empty_matches=True)]
    matches["_id"] = matches.pop("id")

def get_hopefuls(session, limit=10):
    """
    Return a list of user dictionaries from hopefuls.

    Likes them on the way in :)
    """
    result = []
    hopefuls = session.nearby_users(limit=limit)
    for hopeful in hopefuls:
        hopeful.like()
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

    session = pynder.Session("1165230333",
                             "CAAGm0PX4ZCpsBAIXjO1ARhwBjiUtQpMc1JfKO8M82QIO8SVPmmZCCX0ZBYhBnV8689dRlDRsAGEWsomBj858o0OC3ZCqG0tCRm6ZA8IuRbHiQ9AxxJyHyFJwR2eh20xEpOZAyZAAaJ684JKhQpmX3ZBUAmHGWDfFAyzk3Aepuro9VUW7v18QaXgJ6ZCULxXy43HHBHBwMUOsR5kNi9l3V1HDRsBRtvmuVZABLtiL8ZCnbe8DCXuBK6NkePk")
    client = MongoClient()
    db = client.tinderp
    match_collection = db.matches
    hopefuls_collection = db.hopefuls

    hopefuls = get_hopefuls(session, limit=100)
    while hopefuls:
        print("liked {} people".format(len(hopefuls)))
        for hopeful in hopefuls:
            persist(hopefuls_collection, hopeful)

        hopefuls = get_hopefuls(session, limit=100)
