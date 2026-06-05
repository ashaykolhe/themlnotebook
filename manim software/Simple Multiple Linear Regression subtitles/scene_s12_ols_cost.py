# -*- coding: utf-8 -*-
# S12 - OLS Cost Function
# Run: manim -pqh scene_s12_ols_cost.py Scene_s12_ols_cost
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s12_ols_cost(LinearRegressionVideo):
    def construct(self):
        self.s12_ols_cost()
