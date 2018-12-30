# mosquito-monitoring
Identify mosquito species and collect data to anticipate epidemics propagation
for a CentraleSupelec project

Deployed app (old) : [mosquito-monitor.herokuapp.com](https://mosquito-monitor.herokuapp.com)   
Deployed app (our own server with persistent database, temporary url) : [mosquito.paulasquin.com](http://mosquito.paulasquin.com) 
# Introduction
## Project purpose
This project aims to monitor and later anticipate mosquito related epidemics.
Crossing the information about mosquito species, localization, temperature and population density may be really powerful to intuite the evolution or the apparition of an epidemic. Thus, we want to create a plateform where anyone can participate to this big-scale survey.

The user can upload a mosquito picture and will be asked to provide additional information as they localization or the mosquito species if known.
Those information will be written in a database, and a Machine Learning algorithm will try to identify where the mosquito is located in the image and what is its species. 

## Project graph
![Project Graph](docs/graph_project.png) 

We initiated a Dockerfile and a docker-compose.yml file in order to wrap all the requirements and dependancies of this project.

You have then 2 choices:

- The 1st one is to install all the requirements (see Installation below)
- The second one is to have Docker (version 1.13.0+ and above) installed and running on your OS


## Installation (only if you are not using Docker)

NB: You need to have python 3.6 installed and **not** 3.7 installed on your machine.

```bash
git clone https://github.com/mosquito-boys/mosquito-monitoring.git
cd mosquito-monitoring
pip3 install -r requirements.txt
```

You may have to install some additional libraries for opencv.

## Start server

The server will listen on port 5000.
You will need a Google Vision API Key written in the .env file. 
You will have to create this file at the root of the project, like : 

```bash
#.env
GOOGLE_APPLICATION_CREDENTIALS=YOUR_KEY
```


### With Docker
Be sure to have docker and docker-compose installed. If you haven't them already, you can follow those tutorials for [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/).  
Then run  
```bash
git clone https://github.com/mosquito-boys/mosquito-monitoring.git
cd mosquito-monitoring
# You should copy in this directory the .env file with your API keys, then run
sudo docker-compose up
```

If you want to rebuild the project you can run 

```bash
docker-compose build
```

### With Docker on a server

If you want to start the project on your server startup, you can follow this procedure:
```bash
cd ~
# Working in personal folder
git clone https://github.com/mosquito-boys/mosquito-monitoring.git
cd mosquito-monitoring
```
You should copy in this directory the .env file with your API keys.  
Also, in order to enable the systemctl service, you will have to edit the [docker-mosquito.service](docker-mosquito.service).
```WorkingDirectory=/home/USERNAME/mosquito-monitoring``` by replacing ```USERNAME``` with your server username.  
Note : we didn't indicate to use /var/www/ as the ```.env``` may be exposed.
Then run:
```bash
sudo docker-compose -f docker-compose-ssl.yml build
sudo cp docker-mosquito.service /etc/systemd/system
sudo systemctl enable docker-mosquito
sudo systemctl restart docker-mosquito
```
This last command will run docker-compose -f docker-compose-ssl.yml up


Note: the project support ssl certificates! You can edit [docker-compose-ssl.yml](docker-compose-ssl.yml) to mount your own certificates.  
Ours were generated with [Let's Encrypt](https://letsencrypt.org/)  

### Without Docker
Debug mode
```
FLASK_APP=server.py FLASK_DEBUG=1 python3 -m flask run
```
Normal mode
```
python3 server.py
```

## Label a mosquito
Import the mosquito classification module
```
import classification.command_classification as command_classification
```

Request the labelling
```
command_classification.label_automatic(path_img)
```

Return example 
```
[['aedes', '0.8780854'], ['culex', '0.11636846'], ['anopheles', '0.0055461014']]
```

## Additional commands

Remove the database (useful for development purpose)

```
rm ./sqlite.db
```

Freeze local packages into requirements.txt with following command

```
pipreqs ./ --force      
```

# Run the tests

Don't run directly the scripts independently.
To test them, run the corresponding test script like below:

```
python3 -m tests.my_test
```

## Retrain

To run a retrain of Inception

```
python3 -m tests.test_command_classification --retrain
```
You shall now wait for 3 to 7 minutes depending on your CPU

## Prediction

To run an image labelling test

```
python3 -m tests.test_command_classification --label [optional path to one or more images]
```
Ouput :

```
Testing image labelling
/home/paul/Projects/POOA/mosquito-monitoring/classification/tensorflow
['/home/paul/Projects/POOA/mosquito-monitoring/classification/tensorflow/export_1/graph.db']
['/home/paul/Projects/POOA/mosquito-monitoring/classification/tensorflow/export_1/labels.txt']
['/home/paul/Projects/POOA/mosquito-monitoring/classification/tensorflow/export_1/cmd.txt']
python3 /home/paul/Projects/POOA/mosquito-monitoring/classification/label_image.py --graph=/home/paul/Projects/POOA/mosquito-monitoring/classification/tensorflow/export_1/graph.db --labels /home/paul/Projects/POOA/mosquito-monitoring/classification/tensorflow/export_1/labels.txt --input_layer=Placeholder --output_layer=final_result --image /home/paul/Projects/POOA/mosquito-monitoring/dataset/aedes/pic_001.jpg
2018-10-23 14:28:34.619292: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[['aedes', '0.8780854'], ['culex', '0.11636846'], ['anopheles', '0.0055461014']]

```



# Project Slides
![Slide 1](docs/slide_1.png) 
![Slide 2](docs/slide_2.png) 
