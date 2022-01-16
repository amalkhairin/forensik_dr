import numpy as np
from sklearn.decomposition import PCA

class Container(object):
    def __init__(self):
        self.container = []
        return
    def get_length(self):
        return self.container.__len__()
    
    def append_block(self, newData):
        self.container.append(newData)
        return

    # sort lexicographic
    def sort_by_features(self):
        self.container = sorted(self.container, key=lambda x: (x[1], x[2]))
        return

    def print_all_container(self):
        for index in range(0, self.container.__len__()):
            print(self.container[index])
        return

    def print_container(self, count):
        print(f"Element's index: {self.get_length()}")
        if count > self.get_length():
            self.print_all_container()
        else:
            for index in range(0, count):
                print(self.container[index])
        return

class Blocks(object):
    def __init__(self, gray_img_block, rgb_img, x,y, dimen):
        self.gray = gray_img_block
        self.gray_px = self.gray.load()
        if rgb_img is not None:
            self.image_rgb = rgb_img
            self.image_rgb_pixels = self.image_rgb.load()
            self.is_image_rgb = True
        else:
            self.is_image_rgb = False
        self.coordinate = (x, y)
        self.dimen = dimen

    def compute_block(self):
        block_data_list = []
        block_data_list.append(self.coordinate)
        block_data_list.append(self.compute_characteristic_features(precision=4))
        block_data_list.append(self.compute_pca(precision=6))
        return block_data_list
	
    def compute_pca(self, precision):
        pca_module = PCA(n_components=1)
        if self.is_image_rgb:
            image_array = np.array(self.image_rgb)
            red_feature = image_array[:, :, 0]
            green_feature = image_array[:, :, 1]
            blue_feature = image_array[:, :, 2]

            concatenated_array = np.concatenate((red_feature, np.concatenate((green_feature, blue_feature), axis=0)), axis=0)
            pca_module.fit_transform(concatenated_array)
            components = pca_module.components_
            precise = [round(element, precision) for element in list(components.flatten())]
            return precise
        else:
            image_array = np.array(self.gray)
            pca_module.fit_transform(image_array)
            components = pca_module.components_
            precise = [round(element, precision) for element in list(components.flatten())]
            return precise
    
    def compute_characteristic_features(self, precision):
        characteristic_feature_list = []

        # variable to compute characteristic features
        c4_part1 = 0
        c4_part2 = 0
        c5_part1 = 0
        c5_part2 = 0
        c6_part1 = 0
        c6_part2 = 0
        c7_part1 = 0
        c7_part2 = 0

        """ Compute c1, c2, c3 according to the image block's colorspace """

        if self.is_image_rgb:
            sum_of_red_pixel_value = 0
            sum_of_green_pixel_value = 0
            sum_of_blue_pixel_value = 0
            # compute sum of the pixel value
            for y_coordinate in range(0, self.dimen):
                for x_coordinate in range(0, self.dimen):
                    tmp_red, tmp_green, tmp_blue = self.image_rgb_pixels[x_coordinate, y_coordinate]
                    sum_of_red_pixel_value += tmp_red
                    sum_of_green_pixel_value += tmp_green
                    sum_of_blue_pixel_value += tmp_blue

            sum_of_pixels = self.dimen * self.dimen
            sum_of_red_pixel_value = sum_of_red_pixel_value / \
                (sum_of_pixels)  # mean from each of the colorspaces
            sum_of_green_pixel_value = sum_of_green_pixel_value / \
                (sum_of_pixels)
            sum_of_blue_pixel_value = sum_of_blue_pixel_value / (sum_of_pixels)

            characteristic_feature_list.append(sum_of_red_pixel_value)
            characteristic_feature_list.append(sum_of_green_pixel_value)
            characteristic_feature_list.append(sum_of_blue_pixel_value)

        else:
            characteristic_feature_list.append(0)
            characteristic_feature_list.append(0)
            characteristic_feature_list.append(0)

        """ Compute  c4, c5, c6 and c7"""
        for y_coordinate in range(0, self.dimen):  # compute the part 1 and part 2 of each feature characteristic
            for x_coordinate in range(0, self.dimen):
                # compute c4
                if y_coordinate <= self.dimen / 2:
                    c4_part1 += self.gray_px[x_coordinate, y_coordinate]
                else:
                    c4_part2 += self.gray_px[x_coordinate, y_coordinate]
                # compute c5
                if x_coordinate <= self.dimen / 2:
                    c5_part1 += self.gray_px[x_coordinate, y_coordinate]
                else:
                    c5_part2 += self.gray_px[x_coordinate, y_coordinate]
                # compute c6
                if x_coordinate - y_coordinate >= 0:
                    c6_part1 += self.gray_px[x_coordinate, y_coordinate]
                else:
                    c6_part2 += self.gray_px[x_coordinate, y_coordinate]
                # compute c7
                if x_coordinate + y_coordinate <= self.dimen:
                    c7_part1 += self.gray_px[x_coordinate, y_coordinate]
                else:
                    c7_part2 += self.gray_px[x_coordinate, y_coordinate]

        characteristic_feature_list.append(
            float(c4_part1) / float(c4_part1 + c4_part2))
        characteristic_feature_list.append(
            float(c5_part1) / float(c5_part1 + c5_part2))
        characteristic_feature_list.append(
            float(c6_part1) / float(c6_part1 + c6_part2))
        characteristic_feature_list.append(
            float(c7_part1) / float(c7_part1 + c7_part2))

        precise_result = [round(element, precision)for element in characteristic_feature_list]
        return precise_result
