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

CM = confusion_matrix(img1, img2)
fpp = CM.sum(axis=0) - np.diag(CM)
fnn = CM.sum(axis=1) - np.diag(CM)
tpp = np.diag(CM)
tnn = CM.sum() - (FP + FN + TP)

# Sensitivity, hit rate, recall, or true positive rate
TPR = TP/(TP+FN)
# Specificity or true negative rate
TNR = TN/(TN+FP)
# Precision or positive predictive value
PPV = TP/(TP+FP)
# Negative predictive value
NPV = TN/(TN+FN)
# Fall out or false positive rate
FPR = FP/(FP+TN)
# False negative rate
FNR = FN/(TP+FN)
# False discovery rate
FDR = FP/(TP+FP)

# Overall accuracy
ACC = (TP+TN)/(TP+FP+FN+TN)
# print(fpp, fnn, tpp, tnn)
print('''
    Accuracy: {1}
    MSE     : {2}
    TPR     : {3}
    TNR     : {4}
    FPR     : {5}
    FNR     : {6}
'''.format(ACC, mse, TPR, TNR, FPR, FNR))

print("Akurasi: ", acc)
print("fpr: ", fpr)
