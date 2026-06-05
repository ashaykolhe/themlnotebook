# -*- coding: utf-8 -*-
# S27 - Outliers Leverage
# Run: manim -pqh scene_s27_outliers.py Scene_s27_outliers
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s27_outliers(LinearRegressionVideo):
    def construct(self):
        self.s27_outliers()
