# -*- coding: utf-8 -*-
# S45 - Gradient Descent Steps
# Run: manim -pqh scene_s45_gd_steps.py Scene_s45_gd_steps
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s45_gd_steps(LinearRegressionVideo):
    def construct(self):
        self.s45_gd_steps()
