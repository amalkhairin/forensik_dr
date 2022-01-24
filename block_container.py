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
        block_data_list.append(self.compute_pca(precision=6))
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
