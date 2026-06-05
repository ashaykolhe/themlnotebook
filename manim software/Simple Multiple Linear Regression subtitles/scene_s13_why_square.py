# -*- coding: utf-8 -*-
# S13 - Why Square the Errors
# Run: manim -pqh scene_s13_why_square.py Scene_s13_why_square
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s13_why_square(LinearRegressionVideo):
    def construct(self):
        self.s13_why_square()
