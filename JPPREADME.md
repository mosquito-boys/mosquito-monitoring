# mosquito-monitoring
Identify mosquito species and collect data to anticipate epidemics propagation
for a CentraleSupelec project

**Important links**
[Github Repository](https://github.com/mosquito-boys/mosquito-monitoring)       
Deployed app (our own server with persistent database, temporary url) : [mosquito.paulasquin.com](http://mosquito.paulasquin.com)   
Deployed app (old) : [mosquito-monitor.herokuapp.com](https://mosquito-monitor.herokuapp.com)

## Project purpose
This project aims to monitor and later anticipate mosquito related epidemics.
Crossing the information about mosquito species, localization, temperature and population density may 
be really powerful to intuit the evolution or the apparition of an epidemic. 
Thus, we want to create a plateform where anyone can participate to this big-scale survey.

The user can upload a mosquito picture and will be asked to provide additional 
information as they localization or the mosquito species if known.
Those information will be written in a database, and a Machine Learning algorithm will try 
to identify where the mosquito is located in the image and what is its species. 

## Project graph
![Project Graph](docs/graph_project.png) 

We initiated a Dockerfile and a docker-compose.yml file in order to wrap all 
the requirements and dependencies of this project.

You have then 2 choices:

- The 1st one is to install all the requirements (see Installation below)
- The second one is to have Docker (version 1.13.0+ and above) installed and running on your OS

## Installation


## Start server

The server will listen on port 5000. 
So after having run the server, you will be able to see the project at [127.0.0.1:5000](127.0.0.1:5000)

### With Docker

#### Building the project

```bash
docker-compose build
```

#### Running the project

```bash
docker-compose up
```

### Without Docker

NB: You need to have python 3.6 installed and **not** 3.7 installed on your machine.

#### Installation of dependencies
```bash
pip3 install -r requirements.txt
```

You may have be asked to install some additional libraries for opencv.

#### Run the server

```
python3 server.py
```

## Webapp usage

There are 3 tabs.

### Home tab

This tab let you upload a mosquito that you want to identify.
We suggest you to choose a mosquito picture from the dataset/test folder.
You can use your own location or enter a custom one. For instance you can try the following locations :
44.082189, 26.922443
44.082189, 26.922443
24.400253, 84.642478
0.729654, 115.094303
27.683107, 115.890004
17.212302, -94.212233
8.488606, -74.993682

### Info tab
Is just an information page about the project aims and the team who realised it.

### Map tab
Show a map with all mosquitoes found so far. The db is initialized with 3 mosquitoes, so you can use the map feature.
The map feature use the sqlite db to get all mosquitoes

## Code explanations

### flask server

server.py create the server and launch it with the routes.
The /postform is the main route uploading the mosquito formular, running the prediction and returning the results.
static folder contains resources which are immediately available from the client (localhost:5000/static/...)
We put in the static/tmp folder the pictures of the mosquitoes processed. The utilities/LRU.py script watch this folder and remove old pictures when size exceed 4.
templates folder contains html templates using jinja syntax.

### db_model

Classes which represent the objects used in the project and the corresponding model for the database.
The db is an SQLite database created automatically when the server is launched in a SQLite.db file.
Every successful upload leads to the creation of a user, a mosquito and store them in the db.

At the first start of the server, the sqlite db is created and 3 mosquitoes are stored in it to let you enjoy the map feature (check use the webapp part)

### dataset

#### training and testing

dataset/training contains the initial training dataset
dataset/test contains picture for you to test.

Use the test dataset to test the webapp!

#### dataset_to_be_validated

Uploaded mosquito pictures from users. Some expert should check it and decide the right label for the picture to be added to the dataset.

#### preprocess dataset

In order to be used efficiently, the dataset should be preprocessed (zoom on the mosquito in the picture)
```
python3 preprocess_dataset.py
```
This command preprocess all the pictures from the training dataset and put them in the preprocessed_dataset folder.  
If pictures are detected to have already been preprocessed, 
the script will keep the existing picture and save API requests and pass to the next file.

### classification

Scripts and classes for classification purpose (preprocessing, training, prediction)

#### train the model
Run this command to train the model with the preprocess dataset
```
python3 -m tests.test_command_classification --retrain
```

#### Label a mosquito
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



### utilities

contains some classes useful for the project
EnvReader.py => read the .env file 
Errors.py => some custom Exception classes
LRU.py => multithreaded class that watch the static/tmp folder and remove the oldest files when the maximum size of 4 files is exceeded
 

# Project Slides
![Slide 1](docs/slide_1.png) 
![Slide 2](docs/slide_2.png) 
