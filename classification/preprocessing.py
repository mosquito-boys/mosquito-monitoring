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

# Libraries and environment setting
import requests
import base64
import cv2
import os
import glob

from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists


class Preprocessing():

    @staticmethod
    def mosquito_position(image_path):
        # retrieves coordinates of 4 points in the image framing the mosquito
        # (image width pct for x,  image length pct for y)
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
        response = response.json()["responses"][0]["localizedObjectAnnotations"]

        coords = None
        for res in response:
            if res['name'] == 'Insect':  # only fetching the first insect labeled objects
                coords = res["boundingPoly"]["normalizedVertices"]
                break
        if coords is None:
            print('No insect was found on the picture')
        else:
            return coords

    @staticmethod
    def mosquito_croping(coords, image_path):
        # crops the image around the mosquito and resizes the image into a square
        img = cv2.imread(image_path)

        pt1 = (int(coords[0]["x"] * len(img[0])), int(coords[0]["y"] * len(img)))
        pt2 = (int(coords[2]["x"] * len(img[0])), int(coords[2]["y"] * len(img)))

        crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]

        dim = (150, 150)
        crop_img = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
        return crop_img

    @staticmethod
    def mosquito_framing(coords, image_path):
        # appends a black rectangle around the mosquito
        img = cv2.imread(image_path)

        pt1 = (int(coords[0]["x"] * len(img[0])), int(coords[0]["y"] * len(img)))
        pt2 = (int(coords[2]["x"] * len(img[0])), int(coords[2]["y"] * len(img)))

        cv2.rectangle(img, pt1, pt2, (0, 0, 0), thickness=1, lineType=8, shift=0)

        return img

##Test

# image_path = 'dataset/aedes/pic_009.jpg'
# saving_path = 'preprossing_test_img/'
# coords = preprocessing.mosquito_position(image_path)
# cv2.imwrite(saving_path + 'framed_pic_009.jpg',preprocessing.mosquito_framing(coords, image_path))
# cv2.imwrite(saving_path + 'croped_pic_009.jpg',preprocessing.mosquito_croping(coords, image_path))
# preprocessing.mosquito_croping(coords, image_path)
