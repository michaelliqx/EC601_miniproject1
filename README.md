# EC601_miniproject1 & miniproject3
## I divide the project into three parts.
#### 1.download the tweet and it's picture
#### 2.turn the picture into a video
#### 3.to use the Google Cloud Vision to recognize the fiture of each picture

## First Part:
- in the first part,I use the module of tweepy and the Twitter API to access into the data of twitter, using the api.user_timeline() to get a specific user's twitter, what we get will be a list, which contains all the information about this twitter massage. What we need to do is to find the label of "media_url", which is the website of the picture of this twitter, and then download it. By the way, after download the picture, I have uniformed the size of the pictures.Because when we transfer the picture into a video, some picture with a size of a odd number will result in the failure. 

## Second Part:
- In this part, I have used the os.system() in the os module. It can execute a terminal command in python. And in the command, I used ffmpeg to transfer. what I need to do is to set the parameter of the video and the picture it need.

## Third Part:
- In this part, I need to use the Google Cloud Vision to detect the labels of my picture.It required me to import the google.cloud module to use it. What I set here was to detect the top 3 labels for each picture, which means it's the most related to the pictures' label in Google's data.To be honest, the code of this part, you can find on the official website of Google Cloud Vision and you can use it and change it into what you want it be. The Google supplied the functions,codes and API for users and we just need to know how to use it.  

## miniproject3 update
- In miniproject3, we add some functions to miniproject1 program.
- I used the mysql and mongoDB to upload the label and the tweeter user's information into the database. you could search the data in database by importing my .py file.

- here is the introduce of functions about database in my program:

### MySQL:
1. connectdb(): to connect a database whose username is "lqx", password:"1234567" based on the database:"lqx" on port "3306".
2.createtable(): to create a table to store the data in from the python program, which contains as follows: a sequencial id number for each picture, the tweet user's name, the 3 highest label of the picuture, if no enough label, it will be none.
3.insertdb(): to insert the data into the table.
4.printdb(): to print the data stored in database of specific keyword. the keyword could be selected by any user.

### MongoDB:
1.create_mongodb():connect to local mongoDB and create a database "lqx"
2.if_database(): to make sure the database exist.
3.create_col(): to create a collection
4.if_col(): to make sure if the collection exist
5.mongodb_insert(): to insert the data into the database. the data inputed was the same as inputed into mysql.
6.mongodb_search_all():to search the data in database with specific keywords.
7.delete_statistic():to delete the data in database.

### to be continued...
