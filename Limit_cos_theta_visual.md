# Visualising a Trigonometric Limit using Python

## Problem
Evaluate the limit:

\[
\lim_{\theta \to \frac{\pi}{2}} \frac{\cos \theta}{\frac{\pi}{2} - \theta}
\]

---

## Objective
To understand the concept of **limits** visually using Python by plotting the function and observing its behaviour as \(\theta\) approaches \(\frac{\pi}{2}\).

---

## Mathematical Intuition
As \(\theta \to \frac{\pi}{2}\):

- \(\cos \theta \to 0\)
- \(\frac{\pi}{2} - \theta \to 0\)

Near \(\frac{\pi}{2}\),
\[
\cos \theta \approx \frac{\pi}{2} - \theta
\]

So the ratio approaches **1**.

---

## Visual Method Using Python

Instead of directly calculating the limit, we plot the function near  
\(\theta = \frac{\pi}{2}\) and observe the trend.

### Python Code Used

```python
import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(1.3, 1.56, 400)
y = np.cos(theta) / (np.pi/2 - theta)

plt.plot(theta, y)
plt.axvline(np.pi/2, linestyle='--')
plt.axhline(1, linestyle='--')

plt.xlabel("θ")
plt.ylabel("Value")
plt.title("Limit of cosθ / (π/2 − θ)")
plt.grid()
plt.show()
```

---

## Observation from the Graph

- As \(\theta\) gets closer to \(\frac{\pi}{2}\),
- The curve approaches the horizontal line **y = 1**
- This visually confirms the limit

---

## Final Answer

\[
\boxed{
\lim_{\theta \to \frac{\pi}{2}} \frac{\cos \theta}{\frac{\pi}{2} - \theta} = 1
}
\]

---

## Conclusion
This visual approach using Python helps in:
- Understanding limits intuitively
- Verifying analytical results
- Building strong conceptual clarity

Using graphs makes abstract concepts like limits easier to understand and remember.
