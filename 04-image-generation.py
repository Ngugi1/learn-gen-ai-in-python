import os
from PIL import Image
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests
load_dotenv()


dalle3client = AzureOpenAI(
    api_version=os.environ["AZURE_IMAGE_GEN_API_VERSION"],
    azure_endpoint=os.environ["AZURE_IMAGE_GENERATION_ENDPOINT"],
    api_key=  os.environ["AZURE_IMAGE_GEN_API_KEY"]
)
response = dalle3client.images.generate(
    model=os.environ["AZURE_IMAGE_GEN_MODEL"],
    prompt="A simple nail polish bottle on a white background",
    n=1,
    style="vivid",
    quality="standard",
)

img_dir = os.path.join(os.curdir, "generated_images")
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
generated_img_url = response.data[0].url
generated_image = requests.get(generated_img_url).content
image_path = os.path.join(img_dir, "generated_image.png")

with open(image_path, "wb") as img_file:
    img_file.write(generated_image)

Image.open(image_path).show()
