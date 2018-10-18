# init_project.py by Mosquito boys project

import glob
import os
import classification.preprocessing as preprocessing


class InitProject():
    def __init__(self):
        print("Initialization of the dataset")
        self.create_preprocessed_dataset()

    def check_create_folder(self, path):
        if not os.path.exists(path):
            print("Creating folder " + path)
            os.mkdir(path)

    def create_preprocessed_dataset(
            self,
            dataset_path="dataset",
            preprocessed_dataset_path="preprocessed_dataset"
    ):
        print("Starting creation of the preprocessed dataset")
        self.check_create_folder(preprocessed_dataset_path)
        labels = [folder.split("/")[-2] for folder in glob.glob(dataset_path + "/*/")]
        print("Found labels: " + str(labels))

        i = 0

        for label in labels:
            print("=== " + label + " ===")
            self.check_create_folder("/".join([preprocessed_dataset_path, label]))
            # getting image names from the folder
            image_names = [file.split("/")[-1] for file in glob.glob(dataset_path + "/" + label + "/*.jp*")]

            for image_name in image_names:
                preprocessed_image_name = "crop_" + image_name
                # generate path for original and preprocessed image
                path_image = "/".join([dataset_path, label, image_name])
                path_preprocessed_image = "/".join([preprocessed_dataset_path, label, preprocessed_image_name])

                # Check if preprocessed was not already done
                if not os.path.exists(path_preprocessed_image):
                    # ask for computing the preprocessed image and to write it at the desired path
                    try:
                        i += 1
                        if i < 3:
                            print("+ Saving preprocessed " + path_preprocessed_image)
                            preprocessing.Preprocessing.save_crop_img(path_image, path_preprocessed_image)
                        else:
                            break
                    except InsectNotFound:
                        print("\tCan't crop the image")
                else:
                    print("o Already preprocessed " + path_preprocessed_image)


InitProject()
