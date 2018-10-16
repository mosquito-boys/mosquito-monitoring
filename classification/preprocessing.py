# # preprocessing.py by Mosquito boys project
#
# from google.cloud import vision
# import os
# from pprint import pprint
#
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google-cloud-credentials.json"
#
#
# def localize_objects(image_path):
#     """Localize objects in the local image.
#
#     Args:
#     path: The path to the local file.
#     """
#     client = vision.ImageAnnotatorClient()
#
#
#     with open(image_path, 'rb') as image_file:
#         content = image_file.read()
#     image = vision.types.Image(content=content)
#
#     objects = client.object_localization(
#         image=image).localized_object_annotations
#
#     pprint(objects)
#     return objects
#
#
# def localize_mosquitoes(image_path):
#     objects = localize_objects(image_path)
#     print('Number of objects found: {}'.format(len(objects)))
#     for object_ in objects:
#         print('\n{} (confidence: {})'.format(object_.name, object_.score))
#         print('Normalized bounding polygon vertices: ')
#         for vertex in object_.bounding_poly.normalized_vertices:
#             print(' - ({}, {})'.format(vertex.x, vertex.y))
#
#
# localize_mosquitoes('dataset/aedes/pic_001.jpg')


import requests
import base64
import cv2
import os
from environs import Env
env = Env()
env.read_env()  # read .env file, if it exists

image_path = 'dataset/aedes/pic_003.jpg'
with open(image_path, 'rb') as image_file:
    content = base64.encodebytes(image_file.read())

url = "https://vision.googleapis.com/v1/images:annotate"

querystring = {"key": os.environ["GOOGLE_APPLICATION_CREDENTIALS"]}

payload = {
    "requests":
        [
            {
                "image": {
                    "content": content.decode("utf8")
                },
                "features": [
                    {
                        "type": "OBJECT_LOCALIZATION",
                        "maxResults": 100,
                        "model": ""
                    }
                ]
            }
        ]
}
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=str(payload), headers=headers, params=querystring)

coords = response.json()["responses"][0]["localizedObjectAnnotations"][0]["boundingPoly"]["normalizedVertices"]

print(coords)

img = cv2.imread(image_path)

pt1 =(int(coords[0]["x"]*len(img[0])), int(coords[0]["y"]*len(img)))
pt2 = (int(coords[2]["x"]*len(img[0])), int(coords[2]["y"]*len(img)))

print(len(img), len(img[0]))
print(pt1)
print(pt2)
cv2.rectangle(img, pt1, pt2, (0, 0, 0), thickness=1, lineType=8, shift=0)

cv2.imshow('image',img)
cv2.waitKey(0)