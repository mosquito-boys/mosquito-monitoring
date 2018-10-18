# init_project.py by Mosquito boys project

import glob
import os
import classification.preprocessing as preprocessing


class InitProject():
    def __init__(self):
        print("Initialization of the dataset")
        self.create_preprocessed_dataset()

    def create_preprocessed_dataset(
            self,
            dataset_path="dataset",
            preprocessed_dataset_path="preprocessed_dataset"
    ):
        print("Starting creation of the preprocessed dataset")
        labels = [folder.split("/")[-2] for folder in glob.glob(dataset_path + "/*/")]
        print("Found labels: " + str(labels))

        for label in labels:
            print("=== " + label + " ===")
            # getting image names from the folder
            image_names = [file.split("/")[-1] for file in glob.glob(dataset_path + "/" + label + "/*.jp*")]

            for image_name in image_names:
                preprocessed_image_name = "crop_" + image_name
                # generate path for original and preprocessed image
                path_image = "/".join([dataset_path, label, image_name])
                path_preprocessed_image = "/".join([preprocessed_dataset_path, label, preprocessed_image_name])

                print(path_image)
                print(path_preprocessed_image)

                # Check if preprocessed was not already done
                if not os.path.exists(path_preprocessed_image):
                    print("\t+ Saving preprocessed " + preprocessed_image_name)
                    # ask for computing the preprocessed image and to write it at the desired path
                    preprocessing.Preprocessing.save_crop_img(path_image, path_preprocessed_image)
                else:
                    print("\to Already preprocessed " + preprocessed_image_name)

                break
            break


InitProject()
