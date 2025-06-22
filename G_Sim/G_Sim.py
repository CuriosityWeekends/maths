import time
import matplotlib.pyplot as plt

# Set fps
fps = 240
fdelay = 1/fps

# Set g (m/s*s)
G = -9.8
g = G*fdelay

yv = 1  # Initial y velocity
y = 10  # Initial y pos
yBloss = 0.8    # Amount of Yvelocity that gets refected on bounce (0-1)

xv = 1  # Initial x velocity
x = 0   # Initial x pos
xBloss=0.8  # Amount of Xvelocity that remains on bounce (0-1)

xs = []
ys = []

while True:
    px = x
    x += xv # changes x
    xs.append(x)

    yv += g
    y += (yv-(g/2)*fdelay) # changes y
    if y < 0:
        ys.append(0)
    else:
        ys.append(y)

    if y<0: # Reduces the yv,xv and reflects yv on bounce (y<0)
        y = abs(y) 
        yv = abs(yv)*yBloss
        xv = abs(xv)*xBloss


    plt.clf()   #Plot print sequences
    plt.plot(xs, ys,color="red" ,label='Object')
    plt.xlabel('Distance')
    plt.ylabel('Hight')
    plt.title('G sim')

    plt.legend()
    plt.grid(True)
    plt.pause(0.0000001)

    print(x, y) # prints current x & y pos of the Object
    time.sleep(fdelay) #delay between frames

    if x-px < 0.1:  # Sees if speed is less than 10cm/s
        time.sleep(5)
        break