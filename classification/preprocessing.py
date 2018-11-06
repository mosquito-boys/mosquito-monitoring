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

    @staticmethod
    def mosquito_position(image_path):
        """
        retrieves coordinates of 4 points in the image framing the mosquito
        (image width pct for x,  image length pct for y)
        :param image_path:
        """
        with open(image_path, 'rb') as image_file:
            content = base64.encodebytes(image_file.read())

        url = "https://vision.googleapis.com/v1/images:annotate"

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

        response = requests.request("POST", url, data=str(payload), headers=headers, params=querystring).json()

        if "responses" not in response.keys():
            raise APIQuotaExceeded()
        else:
            try:
                response = response["responses"][0]["localizedObjectAnnotations"]
            except Exception:
                raise Errors.InsectNotFound

        coords = None
        for res in response:
            if res['name'] == 'Insect':  # only fetching the first insect labeled objects
                coords = res["boundingPoly"]["normalizedVertices"]
                break
        if coords is None:
            print('\tNo insect was found on the picture')
            raise Errors.InsectNotFound
        else:
            return coords

    @staticmethod
    def compute_pt(coords, img):
        """
        Compute pixel points
        :param coords:
        :param img:
        :return pt1, pt2:
        """
        pt1 = (int(coords[0]["x"] * len(img[0])), int(coords[0]["y"] * len(img)))
        pt2 = (int(coords[2]["x"] * len(img[0])), int(coords[2]["y"] * len(img)))
        return pt1, pt2

    @staticmethod
    def mosquito_croping(coords, image_path):
        """
        crops the image around the mosquito and resizes the image into a square
        :param coords:
        :param image_path:
        """

        img = cv2.imread(image_path)
        pt1, pt2 = Preprocessing.compute_pt(coords, img)
        crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        dim = (150, 150)
        crop_img = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
        return crop_img

    @staticmethod
    def mosquito_framing(coords, image_path):
        """
        Put a black rectangle arround the mosquito in the intial picture
        :param coords:
        :param image_path:
        """
        # appends a black rectangle around the mosquito
        img = cv2.imread(image_path)
        pt1, pt2 = Preprocessing.compute_pt(coords, img)
        cv2.rectangle(img, pt1, pt2, (0, 0, 0), thickness=1, lineType=8, shift=0)
        return img

    @staticmethod
    def save_crop_img(coords, path_origin, saving_path):
        """
        find the insect in of the given path image,
        crop the image to the insect and save it in the given preprocessed path
        :param coords:
        :param path_origin:
        :param saving_path:
        """
        crop_img = Preprocessing.mosquito_croping(coords, path_origin)
        cv2.imwrite(saving_path, crop_img)
        return saving_path

    @staticmethod
    def save_framed_img(coords, path_origin, saving_path):
        """
        find the insect in of the given path image,
        crop the image to the insect and save it in the given preprocessed path
        :param coords:
        :param path_origin:
        :param saving_path:
        """
        crop_img = Preprocessing.mosquito_framing(coords, path_origin)
        cv2.imwrite(saving_path, crop_img)
        return saving_path
