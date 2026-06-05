# -*- coding: utf-8 -*-
# S48 - Gradient Descent Pros & Cons
# Run: manim -pqh scene_s48_gd_pc.py Scene_s48_gd_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s48_gd_pc(LinearRegressionVideo):
    def construct(self):
        self.s48_gd_pc()
