import os
import errno
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

search = input("Search for:")
params = {"q": search}
r = requests.get("http://www.bing.com/images/search", params=params)

soup = BeautifulSoup(r.text, "html.parser")
links = soup.findAll("a", {"class": "thumb"})

filename = "./scraped_images/"
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

for item in links:
    img_obj = requests.get(item.attrs["href"])
    print("Getting", item.attrs["href"])
    title = item.attrs["href"].split("/")[-1]
    img = Image.open(BytesIO(img_obj.content))
    img.save("./scraped_images/" + title, img.format)
