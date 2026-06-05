# -*- coding: utf-8 -*-
# S17 - Linearity Assumption Plots
# Run: manim -pqh scene_s17_linearity.py Scene_s17_linearity
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s17_linearity(LinearRegressionVideo):
    def construct(self):
        self.s17_linearity()
