# command_retrain.py

import os
import threading as th
import subprocess

TENSOR_FOLDER = "tensorflow"
IMAGE_DIR = "dataset"


def getExportNumber(tensorFolder):
    """ Arrange the models in different files for monitoring the model versions
    Get the number of the export folder looking at already existing folders
    Handle the presence of '_precisions' at the end of the folder name """

    lesDir = os.listdir(tensorFolder)
    lesExport = []
    lesNum = []
    num = 0
    for dir in lesDir:
        if "export_" in dir:
            lesExport.append(dir)
    for i in range(len(lesExport)):
        # Get number of export and add 1 to it
        # If we have an extension in the name
        if lesExport[i][7:].find("_") != -1:
            lesNum.append(int(lesExport[i][7:7 + lesExport[i][7:].find("_")]))
        # If there is not extension
        else:
            lesNum.append(int(lesExport[i][7:]))

    if len(lesNum) != 0:
        num = max(lesNum) + 1
    return num


class Retrain(th.Thread):
    def __init__(self):
        print("Starting Retrain")
        super(Retrain, self).__init__()
        self._stop_event = th.Event()

    def run(self):
        """
        Retrain the tensorflow model using JPG images
        """

        if not os.path.isdir(TENSOR_FOLDER):
            os.mkdir(TENSOR_FOLDER)
        export_number = getExportNumber(TENSOR_FOLDER)
        export_path = str(TENSOR_FOLDER) + "/export_" + str(export_number)
        os.mkdir(export_path)

        print("export_path : " + export_path)
        if not os.path.isdir(TENSOR_FOLDER):
            os.mkdir(TENSOR_FOLDER)

        cmd = "python3 retrain.py" \
              " --image_dir " + str(IMAGE_DIR) + \
              " --output_graph " + str(TENSOR_FOLDER) + "/imagenet_inception.db" + \
              " --output_labels " + str(TENSOR_FOLDER) + "/imagenet_labels.txt" + \
              " --saved_model_dir " + export_path + "/model/" + \
              " --print_misclassified_test_images" + \
              " --validation_batch_size=-1" + \
              " --how_many_training_steps 4000" + \
              " --summaries_dir retrain_logs/" + \
              " --train_maximum True" #+ \
              #" --validation_percentage 5" + \
              #" --testing_percentage 5"  # + \
        #  " --tfhub_module
        # 'https://tfhub.dev/google/imagenet/pnasnet_large/classification/2'"
        #  https://tfhub.dev/google/imagenet/inception_resnet_v2/classification/1'"

        print("Running retrain : \n" + cmd)
        with open(export_path + "/cmd.txt", 'w') as f:  # saving command for future monitoring
            f.write(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        print(out.decode('utf-8'))
        print("Retrain ended")

    def stop(self):
        self._stop_event.set()


class Tensorboard(th.Thread):
    def __init__(self):
        print("Starting Tensorboard")
        super(Tensorboard, self).__init__()
        self._stop_event = th.Event()

    def run(self):
        cmd = "tensorboard --logdir retrain_logs"
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p1.communicate()
        print(out.decode('utf-8'))

    def stop(self):
        self._stop_event.set()


def main():
    try:
        # Kill precedent residual tensorboard server
        os.system("killall tensorboard")
        # Launch retrain thread
        retrain_thread = Retrain()
        tensorboard_thread = Tensorboard()
        retrain_thread.start()
        tensorboard_thread.start()
        retrain_thread.join()
        tensorboard_thread.join()

        input("Press a key to stop the program and stop tensorboard")

        return 0
    except KeyboardInterrupt:
        retrain_thread.stop()
        tensorboard_thread.stop()
        return 0


if __name__ == "__main__":
    main()
