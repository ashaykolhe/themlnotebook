# -*- coding: utf-8 -*-
# S31 - MSE Pros & Cons
# Run: manim -pqh scene_s31_mse_pc.py Scene_s31_mse_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s31_mse_pc(LinearRegressionVideo):
    def construct(self):
        self.s31_mse_pc()
