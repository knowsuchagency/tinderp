from pymongo import MongoClient
from pathlib import Path
from operator import itemgetter
from io import BytesIO
import requests

if __name__ == "__main__":
    from pprint import pprint
    client = MongoClient()
    col = client.tinderp.hopefuls
    mention_snapchat = list(col.find(
        {'mentions_snapchat': True}
    ))

    for snapper in mention_snapchat:
        # concatenate name of person with their primary key
        name = lambda x: '_'.join(itemgetter('name', '_id')(x))
        name = name(snapper)

        # create a folder for each person
        folder = Path('.', 'photos', name)
        folder.mkdir(exist_ok=True)

        # Create a text file with that person's bio in their folder
        bio = Path(folder, 'bio.txt')
        if not bio.exists():
            bio.write_text(snapper['bio'], encoding='utf8')

        # save photos to that person's folder
        photos = snapper['photos']
        photos.extend(snapper.get('instagram_photos', []))
        for photo_url in photos:
            # wrangle photo name from the url
            name = photo_url.split('/')[-1] if 'instagram' not in photo_url else photo_url.split('/')[-2] + '.jpg'
            path = Path(folder, name)
            if not path.exists():
                photo = requests.get(photo_url)
                path.write_bytes(photo.content)
