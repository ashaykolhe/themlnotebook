# -*- coding: utf-8 -*-
# S19 - Homoscedasticity Equal Variance
# Run: manim -pqh scene_s19_homoscedasticity.py Scene_s19_homoscedasticity
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s19_homoscedasticity(LinearRegressionVideo):
    def construct(self):
        self.s19_homoscedasticity()
