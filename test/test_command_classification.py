# testing command_classification.py
import classification.command_classification as command_classification


def test_command_retrain():
    command_classification.test_and_monitor()


def test_label_image():
    command_classification.label_automatic("/home/paul/Projects/POOA/mosquito-monitoring/dataset/aedes/pic_001.jpg")


if __name__ == "__main__":
    print("Testing command_retrain")
    test_command_retrain()
    print("Testing image labelling")
    test_label_image()
