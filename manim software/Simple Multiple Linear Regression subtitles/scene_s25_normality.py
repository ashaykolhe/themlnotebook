# -*- coding: utf-8 -*-
# S25 - Normality of Residuals
# Run: manim -pqh scene_s25_normality.py Scene_s25_normality
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s25_normality(LinearRegressionVideo):
    def construct(self):
        self.s25_normality()
