# EC601_miniproject1
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
...
...
...
### to be continued...
