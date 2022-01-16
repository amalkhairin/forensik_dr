import cv2
import numpy as np

def addNoise(img, db):
    img_mean = np.mean(img)
    avg_db = 10 * np.log10(img_mean)
    noise_avg_db = avg_db - db
    snr = 10.0 ** (noise_avg_db / 10.0)

    noise = np.random.normal(0, np.sqrt(snr), img.shape)
    return img + noise


image_path = "region_duplication/dataset/img1_tampered.png"
image = cv2.imread(image_path)
i_array = np.array(image / 255)
noisy_image = add_noise(i_array, 40)
noisy_image = np.uint8(noisy_image * 255)
cv2.imshow("Noisy_Image.png", noisy_image)
cv2.waitKey(0)
cv2.imwrite("region_duplication/dataset/noise/Noisy_Image.png", noisy_image)
