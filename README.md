# EC601_miniproject1
#this is the part of access into the twitter and download its picture
consumer_key = '----------------------------------'
consumer_secret = '-------------------------------------'
access_token = '-----------------------------------'
access_secret = '-----------------------------------'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True )


#get the photo from twitter
tweets = api.user_timeline(screen_name='username' , count=100, include_rts=False,exclude_replies=True)
last_id = tweets[-1].id
#to get more twitter
more_tweets = api.user_timeline(screen_name='username', count=100 ,include_rts=False,exclude_replies=True, max_id=last_id - 1)
tweets = tweets + more_tweets

i=1
photos = set()
for t in tweets:
    media = t.entities.get('media', [])
    if (len(media) > 0):
        photos.add(media[0]['media_url'])
#download the photo
for p in photos:
    pic = wget.download(p)
    i += 1
