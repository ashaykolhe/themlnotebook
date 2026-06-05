# -*- coding: utf-8 -*-
# S75 - sklearn Ridge Params
# Run: manim -pqh scene_s75_ridge_params.py Scene_s75_ridge_params
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s75_ridge_params(LinearRegressionVideo):
    def construct(self):
        self.s75_ridge_params()
