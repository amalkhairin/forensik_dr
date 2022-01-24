import cv2
import numpy as np
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import cv2
from PIL import Image


img1 = Image.open("/content/img2_groundtruth_noise40db.png")
img2 = Image.open("/content/img2_noise40db.png")
img1 = img1.getdata()
img2 = img2.getdata()
img1 = np.array([img1])
img2 = np.array([img2])

mse = np.sum((img1.astype(float) - img2.astype(float)) ** 2) / (img1.shape[0] * img2.shape[0])

img1 = img1.flatten()
img2 = img2.flatten()

tnn, fpp, fnn, tpp = confusion_matrix(img1, img2, labels=[0, 1]).ravel()

# fpp = CM.sum(axis=0) - np.diag(CM)
# fnn = CM.sum(axis=1) - np.diag(CM)
# tpp = np.diag(CM)
# tnn = CM.sum() - (fpp + fnn + tpp)

# Sensitivity, hit rate, recall, or true positive rate
TPR = tpp/(tpp+fnn)
# Specificity or true negative rate
TNR = tnn/(tnn+fpp)
# Precision or positive predictive value
PPV = tpp/(tpp+fpp)
# Negative predictive value
NPV = tnn/(tnn+fnn)
# Fall out or false positive rate
FPR = fpp/(fpp+tnn)
# False negative rate
FNR = fnn/(tpp+fnn)
# False discovery rate
FDR = fpp/(tpp+fpp)

# Overall accuracy
ACC = (tpp+tnn)/(tpp+fpp+fnn+tnn)
# print(fpp, fnn, tpp, tnn)
print('''
    Accuracy: {0}
    MSE     : {1}
    TPR     : {2}
    TNR     : {3}
    FPR     : {4}
    FNR     : {5}
'''.format(ACC, mse, TPR, TNR, FPR, FNR))
