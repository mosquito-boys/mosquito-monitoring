# mosquito-monitoring
Identify mosquito species and collect data to anticipate epidemics propagation
for a CentraleSupelec project

Deployment : [https://mosquito-monitor.herokuapp.com/](https://mosquito-monitor.herokuapp.com/)

# Introduction
## Project purpose
The purpose of this project is to be able to monitor and later anticipate mosquito related epidemics.
Crossing the information about mosquito species, localization, temperature and population density may be really powerful to intuite the evolution or the apparition of an epidemic. Thus, we want to create a plateform where anyone can participate to this big-scale survey.

The user can upload a mosquito picture and will be asked to provide additional information as they localization or the mosquito species if known.
Those information will be written in a database, and a Machine Learning algorithm will try to identify where the mosquito is located in the image and what is its species. 

## Project graph
![Project Graph](docs/graph_project.png) 

You need python 3 and the dependencies installed 

# Installation

```
pip3 install -r requirements.txt
```



## Start server

```
FLASK_APP=server.py FLASK_DEBUG=1 python3 -m flask run
```

## Additionnal commands

Remove the database (useful for dev purpose)

```
rm ./sqlite.db
```

Freeze local packages into requirements.txt with following command

```
pipreqs ./ --force      
```

## Run the tests

Don't run directly the scripts independently.
To test them, run the corresponding test script like below:

```
python3 -m tests.my_test
```

# Project Slides
![Slide 1](docs/slide_1.png) 
![Slide 2](docs/slide_2.png) 
