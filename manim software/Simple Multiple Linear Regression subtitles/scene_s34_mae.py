# -*- coding: utf-8 -*-
# S34 - MAE Formula
# Run: manim -pqh scene_s34_mae.py Scene_s34_mae
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s34_mae(LinearRegressionVideo):
    def construct(self):
        self.s34_mae()
