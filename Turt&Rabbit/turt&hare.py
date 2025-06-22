import time
import matplotlib.pyplot as plt

turt = 10 
hare = 0

hare_speed = 1.3
turt_speed = 1

dist_hare = float(0)
dist_turt = float(0)

x_vals = []
hare_vals = []
turt_vals = []

t = float(0)

stx = 0
x = range(0, stx)
yturt = 0
yhare = 0

plt.ion()

while True: 

    stx += 1


    dist_hare = turt - hare
    hare = hare + dist_hare

    t = dist_hare/hare_speed
    dist_turt = t * turt_speed
    turt = turt + dist_turt


    x_vals.append(t)
    hare_vals.append(hare)
    turt_vals.append(turt)

    plt.clf()
    plt.plot(x_vals, hare_vals,color="red" ,label='hare')
    plt.plot(x_vals, turt_vals,color="blue" ,label='turt')
    plt.xlabel('time')
    plt.ylabel('distance')
    plt.title('race between the Turt & the Hare')

    plt.legend()
    plt.grid(True)
    plt.pause(0.1)


    print(hare, turt)
    time.sleep(1)