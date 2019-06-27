# Borathon 2019

## How to run it?

1. Save all your videos in `Zoom videos` folder;
2. Go to `EK docker` folder, run `docker-compose up` to start your ES cluster;
3. Run `python3 vtt2esjson.py` to insert all vtt files in ES;
4. Go to `Flask Server` and start back-end service by `python3 app.py` (change the ip address of es of your own);
5. The server will run on `localhost:6789`

## Briefly describe your idea:

Utility App: Search and find specific words/phrases in a video (or a list of videos eg. confluence videos, youtube etc) and skip through to the relevant contents in the video. Meeting recordings tend to be long and its tedious to skip through it and find that one section you are looking for.

We realize that this application, while it is inspired by experiences of a developer trying to self-educate himself/herself on a topic, it has symptoms of a much broader data retrieval and machine learning problem with applications in things like watching sports game, news conferences and pretty much anything where you do not want to spend the whole time watching the video. For the Borathon, we are targetting the Zoom videos only.

## Problem it will solve?

1. Have you ever wanted to self-educate yourself on a topic and need to go through a bunch of big confluence videos only a single topic you are interested in?
2. What if you wanted to learn a topic but you do not know what confluence videos to watch for it?
3. Do you ever wanted to know all the topics a video touched upon before watching the video?

## List names of all other team members apart from yourself who would be working on this idea (team size are min:4 | max:8)

Pankaj Avhad
Member of Technical Staff

Carolyn Ma
Member of Technical Staff

Honglei Li
Member of Technical Staff

Penghe Zhang
Intern-Product Development-...

Priyankha Bhalasubbramanian
Intern- Product Development...

Pratik Singh
Member of Technical Staff

Varsha Joshi
Member of Technical Staff
