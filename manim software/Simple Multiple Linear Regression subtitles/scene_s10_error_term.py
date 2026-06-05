# -*- coding: utf-8 -*-
# S10 - True Model & Error Term
# Run: manim -pqh scene_s10_error_term.py Scene_s10_error_term
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s10_error_term(LinearRegressionVideo):
    def construct(self):
        self.s10_error_term()
