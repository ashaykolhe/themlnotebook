# -*- coding: utf-8 -*-
# S53 - Lasso Geometric Intuition
# Run: manim -pqh scene_s53_lasso_geometry.py Scene_s53_lasso_geometry
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s53_lasso_geometry(LinearRegressionVideo):
    def construct(self):
        self.s53_lasso_geometry()
