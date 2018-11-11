from classification.preprocessing import Preprocessing

image_path = 'dataset/training/anopheles/pic_014.jpg'

preprocessing = Preprocessing(image_path)

framed = preprocessing.save_framed_img("tests/pic_014_framed.jpg")
crop_resized = preprocessing.save_crop_img("tests/pic_014_cropped.jpg")