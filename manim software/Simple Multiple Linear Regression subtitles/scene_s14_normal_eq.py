# -*- coding: utf-8 -*-
# S14 - Normal Equation Derivation
# Run: manim -pqh scene_s14_normal_eq.py Scene_s14_normal_eq
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s14_normal_eq(LinearRegressionVideo):
    def construct(self):
        self.s14_normal_eq()
