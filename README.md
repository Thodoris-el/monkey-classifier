# monkey-classifier
If you want to use GPU on the requirements.txt comment tensorflow-cpu and uncomment tensorflow

## Intsallation

### Docker (preferred)
* docker build -t monkeyapp .
* docker run -p 5000:5000 monkeyapp
* Go to: http://localhost:5000/

### Local env
* pip install -r requirements.txt
* python app.py
* Go to: http://localhost:5000/

## Description

### Upload a monkey image
You can upload a monkey image and the CNN model will preditc it to one of the 10 labels (alouatta_palliata, erythrocebus_patas, cacajao_calvus, macaca_fuscata, cebuella_pygmea, cebus_capucinus, mico_argentatus, saimiri_sciureus, aotus_nigriceps, rachypithecus_johnii)

### Play A Game
There are some images saved locally. The game shows a random monkey picture and the goal is to guess the label. The CNN model will also predict and we will see who wins.

### Info
There are some information about the monkeys species
