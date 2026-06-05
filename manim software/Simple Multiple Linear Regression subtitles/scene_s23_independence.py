# -*- coding: utf-8 -*-
# S23 - Independence of Errors
# Run: manim -pqh scene_s23_independence.py Scene_s23_independence
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s23_independence(LinearRegressionVideo):
    def construct(self):
        self.s23_independence()
