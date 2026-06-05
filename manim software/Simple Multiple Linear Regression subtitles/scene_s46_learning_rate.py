# -*- coding: utf-8 -*-
# S46 - Learning Rate Convergence Curves
# Run: manim -pqh scene_s46_learning_rate.py Scene_s46_learning_rate
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s46_learning_rate(LinearRegressionVideo):
    def construct(self):
        self.s46_learning_rate()
