# -*- coding: utf-8 -*-
# S67 - Bias Variance Tradeoff Curve
# Run: manim -pqh scene_s67_bv_curve.py Scene_s67_bv_curve
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s67_bv_curve(LinearRegressionVideo):
    def construct(self):
        self.s67_bv_curve()
