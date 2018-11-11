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
be really powerful to predict the evolution or the breakout of an epidemic. 
Thus, we want to create a platform where anyone can participate to this big-scale survey.

The user can upload a mosquito picture and will be asked to provide additional 
information such as their localization or the mosquito species if known.
Those information will be written in a database, and a Machine Learning algorithm will determine where the mosquito is located in the picture and to which species it belongs to.

Our app can recognize 3 mosquito species so far:
- Aedes
- Anopheles
- Culex


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

You may be asked to install some additional libraries for opencv.

#### Run the server

```
python3 server.py
```

## Webapp usage

There are 3 tabs.

### Home tab

This tab let you upload a web form containing a picture of the mosquito you want to identify and other useful informations.

We suggest you to choose a mosquito picture from the dataset/test folder for the mosquito upload.

Then you can add a location by sharing (it with be your current location) or enter it manually. This information will be used for the map feature explained bellow.
You can use your own location or enter a custom one. For instance you can try the following locations :
- 4.082189, 26.922443
- 44.082189, 26.922443
- 24.400253, 84.642478
- 0.729654, 115.094303
- 27.683107, 115.890004
- 17.212302, -94.212233
- 8.488606, -74.993682

Then you can add the date of picture

Finally add you Name (mandatory), Email address (mandatory) and comment (optional) and submit your form

### Info tab

Page containing information about the project goals and the team who realised it.

### Map tab

Show a map with all mosquitoes found so far.
The server get the mosquitos informations in the db to the frontend and we use Google Maps API to generate the map and print mosquitos as markers in the map.

The db is initialized with 3 mosquitoes, so you can use the map feature. But any mosquito you upload with a location will appear on this map.

## Code explanations

### Flask server

We used flask python library to launch the server.

server.py creates the server and launches it with the routes.
The /postform is the main route uploading the mosquito form, running the prediction and returning the results.

static folder contains resources which are immediately available from the client (localhost:5000/static/...)
We put in the static/tmp folder the pictures of the mosquitoes processed.

utilities/LRU.py script keeps an eye on this folder and removes old pictures when size exceeds 4.

templates folder contains html templates using jinja syntax.

### Database model and object representations

In the db_model folder, you can find classes which represent the objects used in the project and the corresponding model for the database.
The db is an SQLite database created automatically when the server is launched in a SQLite.db file.
Every successful upload leads to the creation of a user, a mosquito which are then stored them in the db.

DBEngine is an abstract class that have the minimal methods to be implemented by any database.
We chose SQLite as DB implementation.

At the first start of the server, the sqlite db is created and 3 mosquitoes are stored in it to let you enjoy the map feature (check use the webapp part)

### dataset

#### training and testing

dataset/training contains the initial training dataset
dataset/test contains picture for you to test.

Use the test dataset to test the webapp!

#### dataset/to_be_validated

Uploaded mosquito pictures from users. Some expert should check it and decide on the right label for the picture to be added to the dataset.

#### preprocess dataset

In order to be used efficiently, the dataset should be preprocessed (zoom on the mosquito in the picture)
```
python3 preprocess_dataset.py
```
This command pre-processes all the pictures from the training dataset and puts them in the preprocessed_dataset folder.  
If a pictures has already been preprocessed, 
the script will keep the existing picture and pass to the next file thus saving API requests.

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

contains some useful classes for the project
EnvReader.py => read the .env file 
Errors.py => some custom Exception classes
LRU.py => multithreaded class that watch the static/tmp folder and remove the oldest files when the maximum size of 4 files is exceeded
 

# Project Slides
![Slide 1](docs/slide_1.png) 
![Slide 2](docs/slide_2.png) 
