# -*- coding: utf-8 -*-
# S07 - The Mathematical Model
# Run: manim -pqh scene_s07_math_model.py Scene_s07_math_model
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s07_math_model(LinearRegressionVideo):
    def construct(self):
        self.s07_math_model()
