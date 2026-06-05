# -*- coding: utf-8 -*-
# S66 - Bias Variance Decomposition
# Run: manim -pqh scene_s66_bias_variance.py Scene_s66_bias_variance
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s66_bias_variance(LinearRegressionVideo):
    def construct(self):
        self.s66_bias_variance()
