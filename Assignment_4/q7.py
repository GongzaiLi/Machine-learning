import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs

# we create 40 separable points
X, y = make_blobs(n_samples=40, centers=2, random_state=6)

"""
todo added
make some noise 
The red point is 1 and the blue point is 0
"""
X_noise, y_noise = make_blobs(n_samples=5, centers=2, random_state=6)

X = np.concatenate((X, X_noise), axis=0)
y_noise = [int(not i) for i in y_noise]
y = np.concatenate((y, y_noise), axis=0)


# fit the model, don't regularize for illustration purposes
# clf = svm.SVC(kernel="linear", C=1000)

# Gaussian kernel
# Run the program with different values of C ranging from 10^-2 to 10^5.
# todo https://www.quora.com/What-are-C-and-gamma-with-regards-to-a-support-vector-machine
clf = svm.SVC(kernel='rbf', C=10000)
clf.fit(X, y)

plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)

# plot the decision function
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(
    XX, YY, Z, colors="k", levels=[-1, 0, 1], alpha=0.5, linestyles=["--", "-", "--"]
)
# plot support vectors
ax.scatter(
    clf.support_vectors_[:, 0],
    clf.support_vectors_[:, 1],
    s=100,
    linewidth=1,
    facecolors="none",
    edgecolors="k",
)
plt.show()
"""
1. Instead of creating a perfectly separable dataset, create a "noisy" data where some proportion of 
the points (say 15% to 30% of them) are on the wrong side. You can do this by adding a few lines of 
code after X and y are created and flip some y values from 0 to 1 or 1 to 0.

2. Use a more powerful kernel that is equivalent to the Gaussian kernel discussed in the lecture notes. 
You simply need to find the name of this kernel in the documentation.

3. Run the program with different values of C ranging from 10-2 to 105.
"""
