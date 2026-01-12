# Quadratic Polynomial – Graph using Python

## Polynomial
We are given the quadratic polynomial:

\[
p(x) = x^2 - 4
\]

---

## Objective
To plot the graph of a **quadratic polynomial** using Python and understand its shape and zeros visually.

---

## Python Code Used

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 200)
y = x**2 - 4

plt.plot(x, y, 'g')
plt.axhline(0)   # x-axis
plt.axvline(0)   # y-axis
plt.grid(True)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Quadratic Polynomial : p(x) = x**2 - 4")
plt.show()
```

---

## Observation from the Graph
- The graph is **U-shaped**, which is the shape of a quadratic polynomial.
- The graph cuts the **x-axis at x = -2 and x = 2**.
- Hence, the polynomial has **two zeros**.

---

## Conclusion
This graph confirms that a quadratic polynomial can have **at most two zeros**.  
Plotting the polynomial using Python helps in understanding the concept visually instead of memorizing results.

---

**Day 3 – Python + Maths Streak ✔**
