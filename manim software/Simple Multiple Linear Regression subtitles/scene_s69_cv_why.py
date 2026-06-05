# -*- coding: utf-8 -*-
# S69 - Cross Validation Why
# Run: manim -pqh scene_s69_cv_why.py Scene_s69_cv_why
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s69_cv_why(LinearRegressionVideo):
    def construct(self):
        self.s69_cv_why()
