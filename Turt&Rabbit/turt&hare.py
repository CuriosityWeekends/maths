import time
import matplotlib.pyplot as plt

turt = 10 
hare = 0

hare_speed = 2
turt_speed = 1

dist_hare = float(0)
dist_turt = float(0)

t = float(0)

stx = 0
x = range(0, stx)
yturt = 0
yhare = 0

while True:

    stx += 1
    x = range(0, stx)

    dist_hare = turt - hare
    hare = hare + dist_hare
    #print(dist_hare)
    t = dist_hare/hare_speed
    dist_turt = t * turt_speed
    turt = turt + dist_turt

    plt.clf()
    plt.plot(x, hare,"red" ,label='hare')
    plt.plot(x, turt,"blue" ,label='turt')
    plt.xlabel('time')
    plt.ylabel('distance')
    plt.title('race between the Turt & the Hare')

    plt.legend()
    plt.grid(True)
    plt.draw()
    plt.pause(0.1)


    print(hare, turt)
    time.sleep(1)
