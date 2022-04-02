import requests  # to get image from the web
import shutil  # to save it locally

from app.mongo_client import db


pokemon_coll = db.pokemon

# for i in range(1, pokemon_counts["total"] + 1):
for pokemon in pokemon_coll.find({}):
    image_url = pokemon["sprite"]
    filename = image_url.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print(f"Image sucessfully Downloaded: {filename}")
    else:
        print("Image Couldn't be retreived")
