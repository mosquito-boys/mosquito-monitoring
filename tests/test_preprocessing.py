import os
import classification.preprocessing as pre
import cv2

image_path = 'dataset/anopheles/pic_014.jpg'

coords = pre.Preprocessing.mosquito_position(image_path)

framed = pre.Preprocessing.mosquito_framing(coords, image_path)
crop_resized = pre.Preprocessing.mosquito_croping(coords, image_path)

cv2.imshow('framed', framed)
cv2.waitKey(0)

cv2.imshow('crop_resized', crop_resized)
cv2.waitKey(0)
