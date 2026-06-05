# -*- coding: utf-8 -*-
# S50 - Ridge Cost Function
# Run: manim -pqh scene_s50_ridge.py Scene_s50_ridge
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s50_ridge(LinearRegressionVideo):
    def construct(self):
        self.s50_ridge()
