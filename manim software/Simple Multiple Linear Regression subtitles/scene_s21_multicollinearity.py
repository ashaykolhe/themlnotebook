# -*- coding: utf-8 -*-
# S21 - No Multicollinearity
# Run: manim -pqh scene_s21_multicollinearity.py Scene_s21_multicollinearity
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s21_multicollinearity(LinearRegressionVideo):
    def construct(self):
        self.s21_multicollinearity()
