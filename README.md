There is a scheduled Cloud Task in GCP that runs every morning at 9am Central time. 

*BY PUSHING TO MASTER YOU WILL TRIGGER A CLOUD BUILD DEPLOYMENT*

*High Level Walk through*
* That will execute `entrypoint` in `main.py`.
* Each of MLB, NBA, and WNBA are run sequentially. 
* For each league a file in GCS is read in. This is a map of player IDs to colleges
* Each player's boxscore for each game the previous night is iterated over and converted to something that implements the "Player" base class
* If the player had a "decent" day and they have a college associated with one that is setup in Twitter a "TweetObject" is created
* A tweet per league per school is generated
* That message goes on a pubsub topic `twitter-message-service-pubsub` with the school as an attribute