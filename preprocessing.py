# preprocessing.py by Mosquito boys project

from google.cloud import vision
from environs import Env
import os

env = Env()
env.read_env()

# SECRET_KEY = os.getenv("MY_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-cloud-credentials.json"


def localize_objects(image_path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()


    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    return objects


def localize_mosquitoes(image_path):
    objects = localize_objects(image_path)
    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))


localize_mosquitoes('dataset/aedes/pic_001.jpg')
