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

    @staticmethod
    def mosquito_position(image_path):
        """
        retrieves coordinates of 4 points in the image framing the mosquito
        (image width pct for x,  image length pct for y)
        :param image_path: path of the image to get the position
        """
        with open(image_path, 'rb') as image_file:
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

    @staticmethod
    def __compute_pt(coordinates, img):
        """
        Compute pixel points
        :param coordinates:
        :param img:
        :return pt1, pt2:
        """
        pt1 = (int(coordinates[0]["x"] * len(img[0])), int(coordinates[0]["y"] * len(img)))
        pt2 = (int(coordinates[2]["x"] * len(img[0])), int(coordinates[2]["y"] * len(img)))
        return pt1, pt2

    @staticmethod
    def mosquito_croping(coordinates, image_path):
        """
        crops the image around the mosquito and resizes the image into a square
        :param coordinates: the coordinates of the mosquito
        :param image_path: the path of the picture to transform
        """

        img = cv2.imread(image_path)
        pt1, pt2 = Preprocessing.__compute_pt(coordinates, img)
        crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        dim = (150, 150)
        crop_img = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
        return crop_img

    @staticmethod
    def mosquito_framing(coordinates, image_path):
        """
        Put a black rectangle arround the mosquito in the intial picture
        :param coordinates: the coordinates of the mosquito
        :param image_path: the path of the picture to transform
        """
        # appends a black rectangle around the mosquito
        img = cv2.imread(image_path)
        pt1, pt2 = Preprocessing.__compute_pt(coordinates, img)
        cv2.rectangle(img, pt1, pt2, (0, 0, 0), thickness=1, lineType=8, shift=0)
        return img

    @staticmethod
    def save_crop_img(coordinates, path_origin, saving_path):
        """
        find the insect in of the given path image,
        crop the image to the insect and save it in the given preprocessed path
        :param coordinates: the coordinates of the mosquito
        :param path_origin: the path of the picture to transform
        :param saving_path: where to same the new picture
        """
        crop_img = Preprocessing.mosquito_croping(coordinates, path_origin)
        cv2.imwrite(saving_path, crop_img)
        return saving_path

    @staticmethod
    def save_framed_img(coordinates, path_origin, saving_path):
        """
        find the insect in of the given path image,
        crop the image to the insect and save it in the given preprocessed path
        :param coordinates: the coordinates of the mosquito
        :param path_origin: the path of the picture to transform
        :param saving_path: where to same the new picture
        """
        crop_img = Preprocessing.mosquito_framing(coordinates, path_origin)
        cv2.imwrite(saving_path, crop_img)
        return saving_path
