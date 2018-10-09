# mosquito-monitoring
Identify mosquito species and collect data to anticipate epidemics propagation

## Installation

You need python 3 and the dependencies installed 

```
pip3 -r requirements.txt
```

Info: freeze local packages into requirements.txt with following command

```
pipreqs ./ --force      
```

## Start server

```
FLASK_APP=server.py FLASK_DEBUG=1 python3 -m flask run
```