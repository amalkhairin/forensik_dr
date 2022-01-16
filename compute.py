from tqdm import tqdm
import analyze_func as analyzer
import numpy as np
import numpy as np
import math
import time

class Compute(object):
    def __init__(self, features_container):
      self.name = name
      self.age = age
    
    def run(self):
        # time logging (optional, for evaluation purpose)
        start_timestamp = time.time()
        self.compute()
        timestamp_after_computing = time.time()
        analyzer.Analyze_func.sort()
        timestamp_after_sorting = time.time()
        analyzer.Analyze_func.analyze()
        timestamp_after_analyze = time.time()
        image_result_path = analyzer.Analyze_func.reconstruct()
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
      
