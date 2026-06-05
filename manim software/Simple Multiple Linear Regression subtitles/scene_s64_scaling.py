# -*- coding: utf-8 -*-
# S64 - Feature Scaling Table
# Run: manim -pqh scene_s64_scaling.py Scene_s64_scaling
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s64_scaling(LinearRegressionVideo):
    def construct(self):
        self.s64_scaling()
