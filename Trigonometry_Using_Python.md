# Learning Trigonometry Using Python

## Objective

To understand sine and cosine functions visually using Python by
plotting their graphs, using a slider to change the angle, and observing
automatic movement of points representing **sin(θ)** and **cos(θ)**.

------------------------------------------------------------------------

## Tools Used

-   Python 3.12\
-   NumPy (mathematical calculations)\
-   Matplotlib (graph plotting and slider interaction)

------------------------------------------------------------------------

## How the Program Works

### 1. Angle Generation

Angles from **0° to 360°** are generated and converted into radians
because Python's trigonometric functions work with radians.

### 2. Calculating sin and cos values

Using NumPy, sine and cosine values are calculated for all angles. These
values form fixed curves.

### 3. Plotting the Graphs

The sine and cosine curves are plotted on the graph. These curves remain
constant.

### 4. Moving Dots

Dots are placed on the curves to represent the values of **sin(θ)** and
**cos(θ)** for the selected angle.

### 5. Slider Interaction

A slider is used to change the angle dynamically. When the slider moves,
the angle changes automatically.

### 6. Automatic Update

When the angle changes, the program recalculates sin(θ) and cos(θ) and
moves the dots accordingly.

------------------------------------------------------------------------

## Issues Faced and Solutions

### Issue 1: Matplotlib not installed

**Reason:** Required library was missing.\
**Solution:** Installed using pip.

### Issue 2: Graph not changing

**Reason:** Expected graph to move.\
**Solution:** Learned that graphs stay fixed and only dots move.

### Issue 3: Dot not moving

**Reason:** Canvas was not refreshing automatically.\
**Solution:** Used `fig.canvas.draw_idle()`.

### Issue 4: Runtime Error -- x must be a sequence

**Reason:** Matplotlib requires data as lists.\
**Solution:** Passed values inside lists.

------------------------------------------------------------------------

## Final Working Python Code

``` python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

x_deg = np.linspace(0, 360, 1000)
x_rad = np.radians(x_deg)

y_sin = np.sin(x_rad)
y_cos = np.cos(x_rad)

fig, ax = plt.subplots(figsize=(8, 5))
plt.subplots_adjust(bottom=0.25)

ax.plot(x_deg, y_sin, label="sin x")
ax.plot(x_deg, y_cos, label="cos x")

ax.set_xlim(0, 360)
ax.set_ylim(-1.1, 1.1)
ax.set_xticks(np.arange(0, 361, 30))
ax.set_yticks(np.arange(-1, 1.1, 0.2))
ax.grid(True)

sin_dot, = ax.plot([0], [0], 'go', markersize=10)
cos_dot, = ax.plot([0], [1], 'ro', markersize=10)

ax.set_xlabel("Angle (degrees)")
ax.set_ylabel("Value")
ax.legend()

slider_ax = plt.axes([0.15, 0.1, 0.7, 0.05])
angle_slider = Slider(slider_ax, "Angle (°)", 0, 360, valinit=0)

def update(angle):
    rad = np.radians(angle)
    sin_dot.set_data([angle], [np.sin(rad)])
    cos_dot.set_data([angle], [np.cos(rad)])
    fig.canvas.draw_idle()

angle_slider.on_changed(update)

plt.show()
```

------------------------------------------------------------------------

## Conclusion

This project demonstrates how Python can be used to understand
trigonometric concepts visually. It makes learning interactive, reduces
memorization, and improves conceptual clarity.
