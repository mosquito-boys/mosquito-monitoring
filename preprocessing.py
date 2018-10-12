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
import io

image_path = 'dataset/aedes/pic_001.jpg'
with open(image_path, 'rb') as image_file:
    content = base64.b64encode(image_file.read())

    # content = base64.b64encode(image_file.read())
    # content = image_file.read().encode("base64")
    print(type(content))

url = "https://vision.googleapis.com/v1/images:annotate"

querystring = {"key": "AIzaSyDwM94lr-M6jeiKWh36_oziESXCP0jpujY"}

payload = {
    "requests":
        [
            {
                "image": {
                    "content": str(content)
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

print(response.text)
