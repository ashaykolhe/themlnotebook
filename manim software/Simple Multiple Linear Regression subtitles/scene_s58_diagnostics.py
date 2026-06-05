# -*- coding: utf-8 -*-
# S58 - Residual Diagnostics 4 Plots
# Run: manim -pqh scene_s58_diagnostics.py Scene_s58_diagnostics
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s58_diagnostics(LinearRegressionVideo):
    def construct(self):
        self.s58_diagnostics()
