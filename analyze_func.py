import block_container as bc

from PIL import Image
import imageio
import tqdm

import numpy as np
import math
import time

class Analyze_func(object):
    def __init__(self, path, img_name, output_dir, dimen):
        print(img_name)
        print("Step 1 of 4: Object and variable initialization, ", end='')
        # image parameter
        self.image_output_directory = output_dir
        self.image_name = img_name
        self.image_data = Image.open(path)
        # height = vertical, width = horizontal
        self.image_width, self.image_height = self.image_data.size

        if self.image_data.mode != 'L':  # L means grayscale
            self.is_rgb_image = True
            self.image_data = self.image_data.convert('RGB')
            rgb_image_pixels = self.image_data.load()
            # creates a grayscale version of current image to be used later
            self.image_grayscale = self.image_data.convert('L')
            grayscale_image_pixels = self.image_grayscale.load()

            for y_coordinate in range(0, self.image_height):
                for x_coordinate in range(0, self.image_width):
                    red_pixel_value, green_pixel_value, blue_pixel_value = rgb_image_pixels[
                        x_coordinate, y_coordinate]
                    grayscale_image_pixels[x_coordinate, y_coordinate] = int(0.299 * red_pixel_value) + int(
                        0.587 * green_pixel_value) + int(0.114 * blue_pixel_value)
        else:
            self.is_rgb_image = False
            self.image_data = self.image_data.convert('L')
        
        self.N = self.image_width * self.image_height
        self.dimen = dimen
        self.b = self.dimen * self.dimen
        self.Nb = (self.image_width - self.dimen + 1) * \
            (self.image_height - self.dimen + 1)
        self.Nn = 2  # amount of neighboring block to be evaluated
        self.Nf = 188  # minimum treshold of the offset's frequency
        self.Nd = 50  # minimum treshold of the offset's magnitude

        self.P = (1.80, 1.80, 1.80, 0.0125, 0.0125, 0.0125, 0.0125)
        self.t1 = 2.80
        self.t2 = 0.02

        print(self.Nb, self.is_rgb_image)

        # container initialization to later contains several data
        self.features_container = bc.Container()
        self.block_pair_container = bc.Container()
        self.offset_dictionary = {}
    
    def run(self):
        # time logging (optional, for evaluation purpose)
        start_timestamp = time.time()
        self.compute()
        timestamp_after_computing = time.time()
        self.sort()
        timestamp_after_sorting = time.time()
        self.analyze()
        timestamp_after_analyze = time.time()
        image_result_path = self.reconstruct()
        timestamp_after_image_creation = time.time()

        print("Computing time :", timestamp_after_computing -
              start_timestamp, "second")
        print("Sorting time   :", timestamp_after_sorting -
              timestamp_after_computing, "second")
        print("Analyzing time :", timestamp_after_analyze -
              timestamp_after_sorting, "second")
        print("Image creation :", timestamp_after_image_creation -
              timestamp_after_analyze, "second")

        total_running_time_in_second = timestamp_after_image_creation - start_timestamp
        total_minute, total_second = divmod(total_running_time_in_second, 60)
        total_hour, total_minute = divmod(total_minute, 60)
        print("Total time    : %d:%02d:%02d second" %
              (total_hour, total_minute, total_second), '\n')
        return image_result_path
    
    def compute(self):
        """
        To compute the characteristic features of image block
        :return: None
        """
        print("Step 2 of 4: Computing characteristic features")

        image_width_overlap = self.image_width - self.dimen
        image_height_overlap = self.image_height - self.dimen

        if self.is_rgb_image:
            for i in tqdm.tqdm(range(0, image_width_overlap + 1, 1)):
                for j in range(0, image_height_overlap + 1, 1):
                    image_block_rgb = self.image_data.crop(
                        (i, j, i + self.dimen, j + self.dimen))
                    image_block_grayscale = self.image_grayscale.crop(
                        (i, j, i + self.dimen, j + self.dimen))
                    image_block = bc.Blocks(
                        image_block_grayscale, image_block_rgb, i, j, self.dimen)
                    self.features_container.append_block(
                        image_block.compute_block())
        else:
            for i in range(image_width_overlap + 1):
                for j in range(image_height_overlap + 1):
                    image_block_grayscale = self.image_data.crop(
                        (i, j, i + self.dimen, j + self.dimen))
                    image_block = bc.Blocks(
                        image_block_grayscale, None, i, j, self.dimen)
                    self.features_container.append_block(
                        image_block.compute_block())
    
    def sort(self):
        self.features_container.sort_by_features()
    
    def analyze(self):
        print("Step 3 of 4:Pairing image blocks")
        z = 0
        time.sleep(0.1)
        feature_container_length = self.features_container.get_length()

        for i in tqdm.tqdm(range(feature_container_length - 1)):
            j = i + 1
            result = self.is_valid(i, j)
            if result[0]:
                self.add_dictionary(self.features_container.container[i][0],
                                    self.features_container.container[j][0],
                                    result[1])
                z += 1
    
    def is_valid(self, first_block, second_block):

        if abs(first_block - second_block) < self.Nn:
            i_feature = self.features_container.container[first_block][1]
            j_feature = self.features_container.container[second_block][1]

            # check the validity of characteristic features
            if abs(i_feature[0] - j_feature[0]) < self.P[0]:
                if abs(i_feature[1] - j_feature[1]) < self.P[1]:
                    if abs(i_feature[2] - j_feature[2]) < self.P[2]:
                        if abs(i_feature[3] - j_feature[3]) < self.P[3]:
                            if abs(i_feature[4] - j_feature[4]) < self.P[4]:
                                if abs(i_feature[5] - j_feature[5]) < self.P[5]:
                                    if abs(i_feature[6] - j_feature[6]) < self.P[6]:
                                        if abs(i_feature[0] - j_feature[0]) + abs(i_feature[1] - j_feature[1]) + \
                                                abs(i_feature[2] - j_feature[2]) < self.t1:
                                            if abs(i_feature[3] - j_feature[3]) + abs(i_feature[4] - j_feature[4]) + \
                                                    abs(i_feature[5] - j_feature[5]) + \
                                                    abs(i_feature[6] - j_feature[6]) < self.t2:

                                                # compute the pair's offset
                                                i_coordinate = self.features_container.container[first_block][0]
                                                j_coordinate = self.features_container.container[
                                                    second_block][0]

                                                # Non Absolute Robust Detection Method
                                                offset = (
                                                    i_coordinate[0] -
                                                    j_coordinate[0],
                                                    i_coordinate[1] -
                                                    j_coordinate[1]
                                                )

                                                # compute the pair's magnitude
                                                magnitude = np.sqrt(
                                                    math.pow(offset[0], 2) + math.pow(offset[1], 2))
                                                if magnitude >= self.Nd:
                                                    return 1, offset
        return 0,
    
    def add_dictionary(self, first_coordinate, second_coordinate, pair_offset):
        if pair_offset in self.offset_dictionary:
            self.offset_dictionary[pair_offset].append(first_coordinate)
            self.offset_dictionary[pair_offset].append(second_coordinate)
        else:
            self.offset_dictionary[pair_offset] = [
                first_coordinate, second_coordinate]
    
    def reconstruct(self):
        """
        Reconstruct the image according to the fraud detectionr esult
        """
        print("Step 4 of 4: Image reconstruction")

        # create an array as the canvas of the final image
        groundtruth_image = np.zeros((self.image_height, self.image_width))
        lined_image = np.array(self.image_data.convert('RGB'))

        sorted_offset = sorted(self.offset_dictionary,
                               key=lambda key: len(
                                   self.offset_dictionary[key]),
                               reverse=True)

        is_pair_found = False

        for key in sorted_offset:
            if self.offset_dictionary[key].__len__() < self.Nf * 2:
                break

            if is_pair_found == False:
                print('Found pair(s) of possible fraud attack:')
                is_pair_found = True

            print(key, self.offset_dictionary[key].__len__())

            for i in range(self.offset_dictionary[key].__len__()):
                # The original image (grayscale)
                for j in range(self.offset_dictionary[key][i][1],
                               self.offset_dictionary[key][i][1] + self.dimen):
                    for k in range(self.offset_dictionary[key][i][0],
                                   self.offset_dictionary[key][i][0] + self.dimen):
                        groundtruth_image[j][k] = 255

        if is_pair_found == False:
            print('No pair of possible fraud attack found.')

        # creating a line edge from the original image (for the visual purpose)
        for x_coordinate in range(2, self.image_height - 2):
            for y_cordinate in range(2, self.image_width - 2):
                if groundtruth_image[x_coordinate, y_cordinate] == 255 and \
                        (groundtruth_image[x_coordinate + 1, y_cordinate] == 0 or
                         groundtruth_image[x_coordinate - 1, y_cordinate] == 0 or
                         groundtruth_image[x_coordinate, y_cordinate + 1] == 0 or
                         groundtruth_image[x_coordinate, y_cordinate - 1] == 0 or
                         groundtruth_image[x_coordinate - 1, y_cordinate + 1] == 0 or
                         groundtruth_image[x_coordinate + 1, y_cordinate + 1] == 0 or
                         groundtruth_image[x_coordinate - 1, y_cordinate - 1] == 0 or
                         groundtruth_image[x_coordinate + 1, y_cordinate - 1] == 0):

                    # creating the edge line, respectively left-upper, right-upper, left-down, right-down
                    if groundtruth_image[x_coordinate - 1, y_cordinate] == 0 and \
                            groundtruth_image[x_coordinate, y_cordinate - 1] == 0 and \
                            groundtruth_image[x_coordinate - 1, y_cordinate - 1] == 0:
                        lined_image[x_coordinate -
                                    2:x_coordinate, y_cordinate, 1] = 255
                        lined_image[x_coordinate, y_cordinate -
                                    2:y_cordinate, 1] = 255
                        lined_image[x_coordinate - 2:x_coordinate,
                                    y_cordinate - 2:y_cordinate, 1] = 255
                    elif groundtruth_image[x_coordinate + 1, y_cordinate] == 0 and \
                            groundtruth_image[x_coordinate, y_cordinate - 1] == 0 and \
                            groundtruth_image[x_coordinate + 1, y_cordinate - 1] == 0:
                        lined_image[x_coordinate +
                                    1:x_coordinate + 3, y_cordinate, 1] = 255
                        lined_image[x_coordinate, y_cordinate -
                                    2:y_cordinate, 1] = 255
                        lined_image[x_coordinate + 1:x_coordinate +
                                    3, y_cordinate - 2:y_cordinate, 1] = 255
                    elif groundtruth_image[x_coordinate - 1, y_cordinate] == 0 and \
                            groundtruth_image[x_coordinate, y_cordinate + 1] == 0 and \
                            groundtruth_image[x_coordinate - 1, y_cordinate + 1] == 0:
                        lined_image[x_coordinate -
                                    2:x_coordinate, y_cordinate, 1] = 255
                        lined_image[x_coordinate, y_cordinate +
                                    1:y_cordinate + 3, 1] = 255
                        lined_image[x_coordinate - 2:x_coordinate,
                                    y_cordinate + 1:y_cordinate + 3, 1] = 255
                    elif groundtruth_image[x_coordinate + 1, y_cordinate] == 0 and \
                            groundtruth_image[x_coordinate, y_cordinate + 1] == 0 and \
                            groundtruth_image[x_coordinate + 1, y_cordinate + 1] == 0:
                        lined_image[x_coordinate +
                                    1:x_coordinate + 3, y_cordinate, 1] = 255
                        lined_image[x_coordinate, y_cordinate +
                                    1:y_cordinate + 3, 1] = 255
                        lined_image[x_coordinate + 1:x_coordinate +
                                    3, y_cordinate + 1:y_cordinate + 3, 1] = 255

                    # creating the straigh line, respectively upper, down, left, right line
                    elif groundtruth_image[x_coordinate, y_cordinate + 1] == 0:
                        lined_image[x_coordinate, y_cordinate +
                                    1:y_cordinate + 3, 1] = 255
                    elif groundtruth_image[x_coordinate, y_cordinate - 1] == 0:
                        lined_image[x_coordinate, y_cordinate -
                                    2:y_cordinate, 1] = 255
                    elif groundtruth_image[x_coordinate - 1, y_cordinate] == 0:
                        lined_image[x_coordinate -
                                    2:x_coordinate, y_cordinate, 1] = 255
                    elif groundtruth_image[x_coordinate + 1, y_cordinate] == 0:
                        lined_image[x_coordinate +
                                    1:x_coordinate + 3, y_cordinate, 1] = 255

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        imageio.imwrite(self.image_output_directory /
                        (timestamp + "_" + self.image_name), groundtruth_image)
        imageio.imwrite(self.image_output_directory /
                        (timestamp + "_lined_" + self.image_name), lined_image)

        return self.image_output_directory / timestamp / "_lined_" / self.image_name
