from requests import get
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait

BASE_URL = "https://www.flipkart.com"
INDEX_URL = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&page={page}"
CONTENT_ROOT_CLASS = "_1HmYoV _35HD7C"
LINK_CLASS = "_31qSD5"
IMAGE_CLASS = "_2_AcLJ"
IMAGE_DIMENSIONS = "800"

def download_image(image_url):
  image_content = get(image_url).content
  filename = image_url[image_url.rfind("/")+1:-5]
  with open(filename, "wb") as file:
    file.write(image_content)

def scrape():
  processed_images = 0
  futures = []
  with ThreadPoolExecutor(max_workers=24) as executor:
    for page_number in range(1, 11):
      content = get(INDEX_URL.format(page=page_number)).content
      soupy_content = BeautifulSoup(content, "html.parser")
      base_of_index = soupy_content.find_all("div", {"class": CONTENT_ROOT_CLASS})[1]
      links_to_phones = base_of_index.find_all("a", {"class": LINK_CLASS})
      for link in links_to_phones:
        stub = link["href"]
        url = BASE_URL + stub
        details_content = get(url).content
        soupy_details = BeautifulSoup(details_content, "html.parser")
        images = soupy_details.find_all("div", {"class": IMAGE_CLASS})
        # Change [images[0]] to images if you want *all* available images.
        for image in [images[0]]:
          image_url = image["style"][21:-1].replace("128", IMAGE_DIMENSIONS)
          futures.append(executor.submit(download_image, image_url))
          processed_images += 1
          print(f"Processed {processed_images}...", end="\r")
  # wait(futures)
  print(f"Downloaded {processed_images}, done.")

if __name__ == "__main__":
  scrape()
