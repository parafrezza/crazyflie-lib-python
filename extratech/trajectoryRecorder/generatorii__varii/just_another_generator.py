import numpy as np
import matplotlib.pyplot as plt

# find the a & b points
def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1

    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B

# returns the general Bezier cubic formula given 4 control points
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])
    
if __name__== '__main__':
    # generate 5 (or any number that you want) random points that we want to fit (or set them youreself)
    points = np.random.rand(5, 2)

    # fit the points with Bezier interpolation
    # use 50 points between each consecutive points to draw the curve
    path = evaluate_bezier(points, 5)
    # extract x & y coordinates of points
    x, y = points[:,0], points[:,1]
    px, py = path[:,0], path[:,1]

    # plot
    # plt.figure(figsize=(11, 8))
    # plt.plot(px, py, 'b-')
    # plt.plot(x, y, 'ro')
    # plt.show()

    from scipy.interpolate import interp1d
    import numpy as np

    # dummy data
    x = np.arange(-100,100,10)
    y = x**2 + np.random.normal(0,1, len(x))

    # interpolate:
    f = interp1d(x,y, kind='cubic')

    # resample at k intervals, with k = 100:
    k = 100
    # generate x axis:
    xnew = np.linspace(np.min(x), np.max(x), k)

    # call f on xnew to sample y values:
    ynew = f(xnew)

    plt.scatter(x,y)
    plt.plot(xnew, ynew)
    plt.show()
