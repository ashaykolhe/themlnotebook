# -*- coding: utf-8 -*-
# S30 - MSE Formula
# Run: manim -pqh scene_s30_mse.py Scene_s30_mse
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s30_mse(LinearRegressionVideo):
    def construct(self):
        self.s30_mse()
