import cv2
import numpy as np

def calculateEvaluationValue(tp, tn, fn, fp):
    TNR = (tn / (fp + tn)) * 100
    TPR = (tp / (tp + tn)) * 100
    FPR = (fp / (fp + tn)) * 100
    acc = ((tp + tn) / (tp + tn + fp + fn)) * 100
    return TNR, TPR, FPR, acc


def calculateValue(img_a, img_b):
    x, y = img_a.shape[0:2]
    tp, tn, fn, fp, = 0, 0, 0, 0
    for i in range(x):
        for j in range(y):
            if sum(img_a[i, j]) == 0 and sum(img_b[i, j]) == 0:
                tn += 1
            elif sum(img_a[i, j]) == 765 and sum(img_b[i, j]) == 765:
                tp += 1
            elif sum(img_a[i, j]) == 0 and sum(img_b[i, j]) == 765:
                fn += 1
            elif sum(img_a[i, j]) == 765 and sum(img_b[i, j]) == 0:
                fp += 1
    return tp, tn, fp, fn


img1_path = "region_duplication/dataset/img1_tampered.png"
img2_path = "region_duplication/dataset/img1_tampered.png"
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)
tp, tn, fp, fn = calculateValue(img1, img2)
tnr, tpr, fpr, acc = calculateEvaluationValue(tp, tn, fn, fp)
print("Akurasi: ", acc)
print("fpr: ", fpr)
