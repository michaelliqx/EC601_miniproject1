#!/usr/bin/env python
import wget
import tweepy
from PIL import Image
from google.cloud import vision
from tweepy import OAuthHandler, TweepError
import ffmpeg
import io
import os
import pymysql
import pymongo



# mysql
###################################################
def connectdb():
    db = pymysql.connect(host= 'localhost',user = 'lqx',password = '1234567',db="lqx",port=3306)
    print(" mysql connect successfully!")
    return db

def createtable(db):
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS lqx")
    sql = '''CREATE TABLE lqx (    ID INT ,
                                    tweeter CHAR(30),
                                    Label1 CHAR(30) ,
                                    Label2 CHAR(30) ,
                                    Label3 CHAR(30) )'''
    cursor.execute(sql)

def insertdb(db,ID,tweeter,Label1,Label2= None,Label3=None):
    cursor = db.cursor()
    sql = '''INSERT INTO lqx(ID,tweeter,Label1,Label2,Label3)VALUE ('%d','%s','%s','%s', '%s')'''%(ID+1,tweeter,Label1,Label2,Label3)
    try:
        cursor.execute(sql)
        db.commit()
        print("insert to mysql successfully")
    except:
        print("fail!")
        db.rollback()

def printdb(db,keywords):
    cursor = db.cursor()
    cursor.execute("select * from lqx where Label1 = '%s' or Label2 = '%s' or Label3 = '%s'"%(keywords,keywords,keywords))
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        tweet_user = row[1]
        label1 = row[2]
        label2 = row[3]
        label3 = row[4]
        print("ID = %d ,Tweet User:%s,label1=%s,label2=%s,label3=%s" %(id,tweet_user,label1,label2,label3))

#############################################

# mongoDB
#############################################
def create_mongodb():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['lqx']


def if_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()
    if "lqx" in dblist:
        print("database lqx exist!")

def create_col():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['lqx']
    mycol = mydb["sites"]

def if_col():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['lqx']
    collist = mydb.list_collection_names()
    if "sites" in collist:
        print("col sites exist")

def mongodb_insert(id,tweeter,label1,label2=None,label3=None):
    usr = 'lqx'
    col = 'sites'
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[usr]
    mycol = mydb[col]
    mydict = {"ID": id+1,'Tweet User':tweeter, "label1": label1, "label2":label2,"label3":label3,'database':str(usr),'collection':str(col)}
    x = mycol.insert_one(mydict)
    print(x)

    # mylist = [
    #     {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
    #     {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
    #     {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
    #     {"name": "Github", "alexa": "109", "url": "https://www.github.com"}
    # ]
    #
    # x = mycol.insert_many(mylist)
    # # 输出插入的所有文档对应的 _id 值
    # print(x.inserted_ids)

def mongodb_search_one():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lqx"]
    mycol = mydb["sites"]
    x = mycol.find_one()
    print(x)

def mongodb_search_all(keywords):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lqx"]
    mycol = mydb["sites"]
    #for x in mycol.find():
    for x in mycol.find({'label1':keywords}):
        print(x)
    for x in mycol.find({'label2': keywords}):
        print(x)
    for x in mycol.find({'label3': keywords}):
        print(x)


def delete_statistic():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lqx"]
    mycol = mydb["sites"]
    # myquery = {"name": "Taobao"}#example
    # mycol.delete_one(myquery)
    # # 删除后输出
    # for x in mycol.find():
    #     print(x)

    mycol.drop()#delete whole "sites"



#############################################



consumer_key = 'P0ZYeebu0IiZ2yXDkJYMKa4QN'
consumer_secret = '1o8drgPRXHxks3FhGLeNJbMXjPf8p3GbE0ywbdlRS1kpGEU5LO'
access_token = '1037401110389174272-6iC08TC3wyhtB3QE5lzaipeM18KYe7'
access_secret = 'TkxumYnCOj8zepySPctzFeKvDS9SFx82gKVjS6evfOjMe'



photos = set()
#get the picture
def getpic(Screen_name,pic_num):
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        tweets = api.user_timeline(screen_name=Screen_name , count=int(pic_num/2), include_rts=False,exclude_replies=True)
        last_id = tweets[-1].id
        more_tweets = api.user_timeline(screen_name=Screen_name, count=pic_num-int(pic_num/2) ,include_rts=False,exclude_replies=True, max_id=last_id - 1)
        tweets = tweets + more_tweets
        i = 1

        for t in tweets:
            media = t.entities.get('media', [])
            if (len(media) > 0):
                photos.add(media[0]['media_url'])
        #download the photo
        for p in photos:
            pic = wget.download(p)
            #rename the photo
            os.renames(pic,str(i)+'.jpg')
            i += 1

        lenth = len(photos)
        thisdir = os.getcwd()
        # normalize the size of the picture

        for j in range(lenth):
            convertjpg(str(j+1) +'.jpg',thisdir)
    except:
        print(TweepError.message[0]['code'])

def convertjpg(newpic,thisdir,width=1200,height=1200):
    img=Image.open(newpic)
    new_img=img.resize((width,height),Image.BILINEAR)
    new_img.save(os.path.join(thisdir,os.path.basename(newpic)))


#generate the video

def video(path):
    os.chdir(path+'\\ffmpeg\\bin')
    cmd ='ffmpeg -framerate .91 -f image2 -i C:/users/lliqx/pycharmprojects/untitled2/%d.jpg  C:/users/lliqx/pycharmprojects/untitled2/label.mp4 '
    os.system(cmd)
    # os.chdir("C:/users/lliqx/pycharmprojects/untitled2")
    cmd2 = 'ffmpeg -i C:/Users/lliqx/PycharmProjects/untitled2/label.srt C:/Users/lliqx/PycharmProjects/untitled2/label.ass'
    cmd3 = 'ffmpeg -i C:/users/lliqx/pycharmprojects/untitled2/label.mp4 -vf subtitles=label.srt C:/users/lliqx/pycharmprojects/untitled2/label.mkv'
    #os.system(cmd2)
    os.system(cmd3)

#get the labels
def detect_labels(path,tweeter):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()
    t = 0
    for i in range(len(photos)):
        Path = path+'\\'+str(i+1) +'.jpg'
        with io.open(Path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations[0:3]
        if len(labels) == 1:
            label2 = 'None'
            label3 = 'None'
        elif len(labels) == 2 :
            label2 = labels[1].description
            label3 = 'None'
        else:
            label2 = labels[1].description
            label3 = labels[2].description
        insertdb(db,i,tweeter,labels[0].description, label2, label3)
        mongodb_insert(i,tweeter,labels[0].description, label2,label3)

        f = open('C:/users/lliqx/pycharmprojects/untitled2/ffmpeg/bin/label.srt', 'a')
        f.write(str(t+1)+'\n')
        f.write('00:00:'+str(t)+'.000 --> 00:00:'+str((t+1))+'.000'+'\n')
        for label in labels:
            f.write(label.description+'\n')
        f.write('\n')
        f.close()
        t += 1

def functions():
    keywords = input("please input the keywords you wanna search:")
    try:
        mongodb_search_all(keywords)
        printdb(db,keywords)
    except:
        print("no such keywords!")


if __name__ == '__main__':
    tweeter = input("input the username:")
    tweets_number = input("input the number of tweeter you want to search:")
    try:
        getpic(tweeter,int(tweets_number))
    except:
        print("no such tweeter!")
        quit()

    db = connectdb()
    createtable(db)
    path = os.getcwd()
    detect_labels(path,tweeter)
    #video(path)

    functions()
    dele = input("do you want to delete the data in mongoDB?(y/n):")
    if dele == 'y':
        delete_statistic()
