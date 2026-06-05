# -*- coding: utf-8 -*-
# S74 - sklearn LinearRegression Params
# Run: manim -pqh scene_s74_lr_params.py Scene_s74_lr_params
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s74_lr_params(LinearRegressionVideo):
    def construct(self):
        self.s74_lr_params()
