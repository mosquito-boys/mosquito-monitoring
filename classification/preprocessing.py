# Libraries and environment setting
import requests
import base64
import cv2
from utilities import Errors
from utilities.EnvReader import get_api_key
from utilities.Errors import APIQuotaExceeded


class Preprocessing:
    """
    Contains methods to target the mosquito in a picture and  crop the picture accordingly
    """

    __API_KEY = get_api_key()
    __API_url = "https://vision.googleapis.com/v1/images:annotate"

    def __init__(self, image_path):
        """
        get mosquito coordinates from google api
        :param image_path: the path of the input picture to preprocess
        """
        self.__image_path = image_path
        # find coordinates
        self.__coordinates = self.__mosquito_position()

    def __mosquito_position(self):
        """
        retrieves coordinates of 4 points in the image framing the mosquito
        (image width pct for x,  image length pct for y)
        :return coordinates: of the found mosquito
        """
        with open(self.__image_path, 'rb') as image_file:
            content = base64.encodebytes(image_file.read())

        querystring = {"key": Preprocessing.__API_KEY}

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

        response = requests.request("POST", Preprocessing.__API_url, data=str(payload), headers=headers, params=querystring).json()

        if "responses" not in response.keys():
            raise APIQuotaExceeded()
        else:
            try:
                response = response["responses"][0]["localizedObjectAnnotations"]
            except Exception:
                raise Errors.InsectNotFound

        coordinates = None

        for res in response:
            if res['name'] == 'Insect':  # only fetching the first insect labeled objects
                coordinates = res["boundingPoly"]["normalizedVertices"]
                break

        if coordinates is None:
            print('\tNo insect was found on the picture')
            raise Errors.InsectNotFound
        else:
            return coordinates

    def __compute_pt(self, img):
        """
        Compute pixel points
        :param img: the np array representing the picture
        :return pt1, pt2:
        """
        pt1 = (int(self.__coordinates[0]["x"] * len(img[0])), int(self.__coordinates[0]["y"] * len(img)))
        pt2 = (int(self.__coordinates[2]["x"] * len(img[0])), int(self.__coordinates[2]["y"] * len(img)))
        return pt1, pt2

    def __mosquito_cropping(self):
        """
        crops the image around the mosquito and resizes the image into a square
        """
        img = cv2.imread(self.__image_path)
        pt1, pt2 = self.__compute_pt(img)
        crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        dim = (150, 150)
        crop_img = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
        return crop_img

    def __mosquito_framing(self):
        """
        Put a black rectangle arround the mosquito in the intial picture
        """
        # appends a black rectangle around the mosquito
        framed_img = cv2.imread(self.__image_path)
        pt1, pt2 = self.__compute_pt(framed_img)
        cv2.rectangle(framed_img, pt1, pt2, (0, 0, 0), thickness=1, lineType=8, shift=0)
        return framed_img

    def save_crop_img(self, saving_path):
        """
        find the insect in of the given path image,
        crop the image to the insect and save it in the given preprocessed path
        :param saving_path: where to same the new picture
        """
        crop_img = self.__mosquito_cropping()
        cv2.imwrite(saving_path, crop_img)
        return saving_path

    def save_framed_img(self, saving_path):
        """
        find the insect in of the given path image,
        crop the image to the insect and save it in the given preprocessed path
        :param saving_path: where to same the new picture
        """
        crop_img = self.__mosquito_framing()
        cv2.imwrite(saving_path, crop_img)
        return saving_path
