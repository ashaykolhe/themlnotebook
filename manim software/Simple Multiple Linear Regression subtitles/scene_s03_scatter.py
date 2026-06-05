# -*- coding: utf-8 -*-
# S03 - House Price Scatter + Best Fit Line
# Run: manim -pqh scene_s03_scatter.py Scene_s03_scatter
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s03_scatter(LinearRegressionVideo):
    def construct(self):
        self.s03_scatter()
