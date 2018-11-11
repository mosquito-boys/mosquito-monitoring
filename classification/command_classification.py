# command_classification.py

import os
import threading as th
import subprocess
import glob
import tensorflow_hub as hub

# Deactivation of Wwrning messages on compiled version
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

TENSOR_FOLDER = "/".join(os.path.realpath(__file__).split("/")[:-1] + ["tensorflow"])
IMAGE_DIR = "/".join(os.path.realpath(__file__).split("/")[:-2] + ["preprocessed_dataset"])
URL_MODULE = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/2"
# "https://tfhub.dev/google/imagenet/pnasnet_large/classification/2"
# "https://tfhub.dev/google/imagenet/inception_resnet_v2/classification/1"

class Retrain(th.Thread):
    def __init__(self, tensor_folder):
        print("Starting Retrain")
        self.tensor_folder = tensor_folder
        super(Retrain, self).__init__()
        self._stop_event = th.Event()

    def run(self):
        """
        Retrain the tensorflow model using JPG images
        """
        if not os.path.isdir(self.tensor_folder):
            os.mkdir(self.tensor_folder)
        export_number = Tools.getExportNumber(self.tensor_folder)
        export_path = str(self.tensor_folder) + "/export_" + str(export_number)
        os.mkdir(export_path)

        print("export_path : " + export_path)
        if not os.path.isdir(self.tensor_folder):
            os.mkdir(self.tensor_folder)
        path_retrain = "/".join(os.path.realpath(__file__).split("/")[:-1] + ["retrain.py"])
        cmd = "python3 " + path_retrain + \
              " --image_dir " + str(IMAGE_DIR) + \
              " --output_graph " + export_path + "/graph.db" + \
              " --output_labels " + export_path + "/labels.txt" + \
              " --saved_model_dir " + export_path + "/model/" + \
              " --bottleneck_dir " + self.tensor_folder + \
              " --print_misclassified_test_images" + \
              " --validation_batch_size=-1" + \
              " --how_many_training_steps 4000" + \
              " --summaries_dir retrain_logs/" + \
              " --train_maximum True" + \
              " --tfhub_module " + URL_MODULE
        # " --validation_percentage 5" + \
        # " --testing_percentage 5"  # + \


        print("Running retrain : \n" + cmd)
        with open(export_path + "/cmd.txt", 'w') as f:  # saving command for future monitoring
            f.write(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        print(out.decode('utf-8'))
        print("Retrain ended")

    def stop(self):
        self._stop_event.set()


class Tools:
    @staticmethod
    def getExportNumber(tensor_folder):

        """ Arrange the models in different files for monitoring the model versions
        Get the number of the export folder looking at already existing folders
        Handle the presence of '_precisions' at the end of the folder name """

        lesDir = os.listdir(tensor_folder)
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


class Tensorboard(th.Thread):
    def __init__(self):
        os.system("killall tensorboard")
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


class Predict:
    """
    Method used to predict the label of an image using generated models.
    """

    @staticmethod
    def get_models(tensor_folder, automatic=True):
        """
        Get the models files paths
        :param tensor_folder:
        :return: graphs_path, labels_path, cmds_path
        """
        if not automatic:
            print(tensor_folder)
        # getting graphs path and processed to alphabetical sort
        graphs_path = glob.glob(tensor_folder + "/*/*.db")
        graphs_path.sort()
        cmds_path = []
        labels_path = []
        for graph in graphs_path:
            labels_path.append("/".join(graph.split("/")[:-1] + ["labels.txt"]))
            cmds_path.append("/".join(graph.split("/")[:-1] + ["cmd.txt"]))
        if not automatic:
            print(graphs_path)
            print(labels_path)
            print(cmds_path)
        return graphs_path, labels_path, cmds_path

    @staticmethod
    def choose_model(tensor_folder, automatic=True):
        """

        :param tensor_folder:
        :param automatic: set to False if you want to be asked to choose a model
        :return: graph_path, labels_path, cmd_path
        """
        graphs_path, labels_path, cmds_path = Predict.get_models(tensor_folder)
        if automatic:
            return graphs_path[-1], labels_path[-1], cmds_path[-1]
        else:
            for i in range(len(graphs_path)):
                print(str(i) + " : " + cmds_path[i])
            id = int(input("Enter number wanted model"))
            if id not in range(len(graphs_path)):
                raise ValueError
            else:
                return graphs_path[id], labels_path[id], cmds_path[id]

    @staticmethod
    def label_image(image_path, tensor_folder, automatic=True):
        """
        Call label_image.py script with a large panel of arguments
        :param image_path:
        :param tensor_folder:
        :param automatic: set to False if you want to be asked to choose a model
        :return: tab with labels and probabilities
        """
        # Generate path to the label_image.py script
        path_label_image = "/".join(os.path.realpath(__file__).split("/")[:-1] + ["label_image.py"])

        # Get the needed file paths :
        # graph for the model
        # labels for the different labels possible
        # cmd for the training parameters
        graph_path, labels_path, cmd_path = Predict.choose_model(tensor_folder, automatic)
        print("Using model " + "/".join(graph_path.split("/")[-3:-1]))

        # Try to get the tfhub_module url from the cmd
        with open(cmd_path, 'r') as cmd_file:
            cmd_content = cmd_file.read().split(" ")
            # Choosing default URL_MODULE
            url_module = URL_MODULE
            try:
                # Try to find the url module as writter in the cmd.txt file
                index_url_module = cmd_content.index("--tfhub_module") + 1
                url_module = cmd_content[index_url_module]
            except ValueError:
                print("Couldn't find tfhub_module url. Trying with the last retrain: " + URL_MODULE)

        print(url_module)
        # Load model specification
        print("Connecting to internet to fetch module spec")
        module_spec = hub.load_module_spec(url_module)

        # Recover the image size expected for this model
        input_height, input_width = hub.get_expected_image_size(module_spec)
        cmd = "python3 " + path_label_image + \
              " --graph=" + graph_path + \
              " --labels " + labels_path + \
              " --input_layer=Placeholder" + \
              " --output_layer=final_result" + \
              " --image " + image_path + \
              " --input_height " + str(input_height) + \
              " --input_width " + str(input_width)

        if not automatic:
            print(cmd)

        # Run the labelling and get the response
        p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = [label.split(" ") for label in out.decode('utf-8').split("\n")[:-1]]
        clean_result = []

        # Changing 1 probability to 100% probability
        for line in result:
            clean_result.append([line[0], str(round(float(line[1]) * 100, 2))])
        return clean_result


def train_and_monitor():
    """
    Start simultaneously a retraining and a tensorboard intstance
    :return:
    """
    print(
        "Starting the training. Enter Ctrl+C at anytime to stop the processes, and in the end to stop tensorboard")

    retrain_thread = Retrain(tensor_folder=TENSOR_FOLDER)
    tensorboard_thread = Tensorboard()
    try:
        retrain_thread.start()
        tensorboard_thread.start()
        retrain_thread.join()
        tensorboard_thread.join()
    except KeyboardInterrupt:
        retrain_thread.stop()
        tensorboard_thread.stop()
        return 0


def label_automatic(path_image):
    """
    Return the probabilities of the labels for a given image in path
    :param path_image:
    :return: prediction with label name and percent of confidence per line
    """
    prediction = Predict.label_image(path_image, TENSOR_FOLDER, automatic=True)
    return prediction
