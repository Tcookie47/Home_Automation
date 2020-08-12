import pyrebase
from firebase import firebase
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
firebase1 = firebase.FirebaseApplication('https://specialtopic-4e64d.firebaseio.com/', None)
db = firebase.database()
def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

my_stream = db.child("posts").stream(stream_handler)
result = firebase1.get('/Status', None)