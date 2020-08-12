import serial
from datetime import datetime
from firebase import firebase
import time 
i =1
a=[]
c=''
ser = serial.Serial('/dev/cu.usbmodem14201', 9600)
time.sleep(1)
def readarduino(ser):
    did=True
    while ser.inWaiting(): # Check number of characters left in buffer
        if did and ser.inWaiting() < 490: # Select last 500 characters in buffer
            for i in range(6):
                print(ser.readline()) # Print 6 lines in buffer
            did = False
        ser.readline()  # Clear buffer line by line until ser.inWaiting goes to 0
readarduino(ser)

data =[]                       # empty list to store the data
firebase = firebase.FirebaseApplication('https://qwerty-fa5d8.firebaseio.com/', None)
while(i):
    b = ser.readline()         # read a byte string
    string_n = b.decode()  # decode byte string into Unicode  
    string = 'kewl' #string_n.rstrip() # remove \n and \r  https://qwerty-611c6.firebaseio.com/

    # flt = float(string)        # convert string to float
    
    print('qwert',string)
    data.append(string)

    print(data)

    if (len(data) == 1):
        c=str(data[0])+'\t'+str(datetime.now())
        print(c)
        result = firebase.post('/LDR', data=c, params={'print': 'pretty'})
        result1 = firebase.post('/TEMP', data=c, params={'print': 'pretty'})
        print(data)
        data =[]
        print ('asdfg',result)
     result = firebase.get('/patient1', '1')
     print(result)          # add to the end of data list
    time.sleep(1)            # wait (sleep) 0.1 seconds
    i=i-1
#readarduino(ser)
#ser.close()



# firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
# result = firebase.get('/patient1', '1')
# print(result)

# result = firebase1.post('/patient1/sensors', data, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# print (result)
# {u'name': u'-Io26123nDHkfybDIGl7'}

# result = firebase1.post('/users', new_user, {'print': 'silent'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# print (result == None)
# True