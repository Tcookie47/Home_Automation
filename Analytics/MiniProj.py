from firebase import firebase
import matplotlib.pylab as plt
import datetime as datetime
firebase1 = firebase.FirebaseApplication('https://specialtopic-4e64d.firebaseio.com/', None)
while(1):

	result = firebase1.get('/Status', None)
	result1 = firebase1.get('/Status1',None)
	print(result)
	print(result1)

	#print(type(result))


	offcount = 0
	oncount = 0
	offcount1 = 0
	oncount1 = 0
	for keys in result.keys():
		if(result[keys] == 'Off'):
			
			offcount = offcount+1
			
		elif(result[keys] == 'On'):
			oncount  = oncount+1
	for keys in result1.keys():
		if(result1[keys] == 'Off'):
			offcount1 = offcount1 + 1
			
		elif(result1[keys] == 'On'):
			oncount1 = oncount1 + 1

	#result = dict(list(result.items())[-5])
	#result1 = dict(list(result1.items())[-5])


	x = list(result.keys())
	x = x[-5:]
	y = list(result.values())
	y = y[-5:]
	x1 = list(result1.keys())
	x1 = x1[-5:]
	y1 = list(result1.values())
	y1 = y1[-5:]
	#x = x[-5]
	#x1 = x1[-5]


	labels = 'Off','On'
	sizes = [offcount,oncount]
	colors = ['lightcoral', 'lightskyblue']
	explode = (0.1, 0.1,)  

	labels1 = 'Off','On'
	sizes1 = [offcount1,oncount1]
	colors1 = ['lightcoral', 'lightskyblue']
	explode1 = (0.1, 0.1,)  



	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

	ax1.plot(x, y,'ro')

	ax2.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.axis('equal')

	ax3.plot(x1,y1,'ro')

	ax4.pie(sizes1, explode=explode1, labels=labels1, colors=colors1,autopct='%1.1f%%', shadow=True, startangle=140)
	ax4.axis('equal')
	plt.show()

