from firebase import firebase
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
firebase1 = firebase.FirebaseApplication('https://manisir-84cd8.firebaseio.com/', None)

#print(result)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102
#tmp102.init()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    result = firebase1.get('/Status', None)

    res = list(result.values())[-1]
    print(res)
    yam = res[0:3]


    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(yam)
    #ys = list(result.keys())

    # Limit x and y lists to 20 items
    xs = xs[-5:]
    ys = ys[-5:]

    # Draw x and y lists
    ax.clear()

    ax.plot(xs, ys, 'ro')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    #plt.title('TMP102 Temperature over Time')
    #plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
