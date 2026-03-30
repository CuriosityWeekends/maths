import numpy as np
import matplotlib.pyplot as plt
plt.ion()

def Polynomial(coefficients, limitsX=(-100, 100)):
    """Returns the x and y values for a polynomial defined by the given coefficients.
    coefficients: A list of coefficients, where the index of the coefficient corresponds to the power of x.
    limitsX: A tuple defining the range of x values to compute.
    """
    x = np.linspace(limitsX[0], limitsX[1], 100)
    y = np.zeros_like(x)
    n = 0
    for coeff in coefficients: 
        y += coeff * (x**n)
        n += 1
        print(n, coeff)
    return x, y

def PolynomialPlot(coefficients, limitsX=(-10, 10)):
    """Plots the polynomial defined by the given coefficients.
    coefficients: A list of coefficients, where the index of the coefficient corresponds to the power of x.
    limitsX: A tuple defining the range of x values to compute.
    """
    x, y = Polynomial(coefficients, limitsX)
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Polynomial Plot')
    plt.grid()
    plt.show()



