# -*- coding: utf-8 -*-
# S65 - Overfitting Underfitting 3 Curves
# Run: manim -pqh scene_s65_overfit.py Scene_s65_overfit
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s65_overfit(LinearRegressionVideo):
    def construct(self):
        self.s65_overfit()
