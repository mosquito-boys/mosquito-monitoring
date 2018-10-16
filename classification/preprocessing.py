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

#Libraries and environment setting
import requests
import base64
import cv2
import os
import glob

from environs import Env


env = Env()
env.read_env()  # read .env file, if it exists


class preprocessing():

    @staticmethod
    def mosquito_position(image_path):
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
        # coordinates of 4 points framing the mosquito
        # in percentage of image width for x and percentage of image length for y
        response = response.json()["responses"][0]["localizedObjectAnnotations"]

        #Fetching coordinates of an insect and not something else
        coords = None
        for res in response:
            if res['name'] == 'Insect':
                coords = res["boundingPoly"]["normalizedVertices"]
                break
            
        return coords
        
    @staticmethod
    def mosquito_croping(coords, image_path):
        img = cv2.imread(image_path)

        pt1 =(int(coords[0]["x"]*len(img[0])), int(coords[0]["y"]*len(img)))
        pt2 =(int(coords[2]["x"]*len(img[0])), int(coords[2]["y"]*len(img)))

        print(len(img), len(img[0]))
        print(pt1)
        print(pt2)
        crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        return crop_img
    
    @staticmethod
    def mosquito_framing(coords, image_path):
        img = cv2.imread(image_path)

        pt1 =(int(coords[0]["x"]*len(img[0])), int(coords[0]["y"]*len(img)))
        pt2 =(int(coords[2]["x"]*len(img[0])), int(coords[2]["y"]*len(img)))

        print(len(img), len(img[0]))
        print(pt1)
        print(pt2)
        cv2.rectangle(img, pt1, pt2, (0, 0, 0), thickness=1, lineType=8, shift=0)

        cv2.imshow('image',img)
        cv2.waitKey(0)

    
    @staticmethod
    def crop_all():
        species_folder = [s.split('/') for s in glob.glob('dataset/*')]
        species = [s[len(s)-1] for s in species_folder]
        for s in species:
            images = [im.split('/') for im in glob.glob('dataset/' + s + '/*.jp*')]
            images = [im[len(im)-1] for im in images]
            
            already_croped_images = [imc.split('/') for imc in glob.glob('dataset_crop/' + s + '/*.jp*')]
            already_croped_images = [imc[len(imc)-1] for imc in already_croped_images]
            for im in images:
                if im in already_croped_images:
                    continue
                relative_path = '/dataset/' + s + '/' +  im
                print(s)
                print(relative_path)
                coords = preprocessing.mosquito_position(relative_path)
                croped = preprocessing.mosquito_croping(relative_path, coords)
                saving_path = '/dataset_crop/' + s + im
                cv2.imwrite(saving_path, croped)

##Test

preprocessing.crop_all()
#image_path = 'dataset/aedes/pic_003.jpg'
#coords = preprocessing.mosquito_position(image_path)

#preprocessing.mosquito_framing(coords, image_path)
#preprocessing.mosquito_croping(coords, image_path)
