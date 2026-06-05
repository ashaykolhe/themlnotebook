# -*- coding: utf-8 -*-
# S60 - Diagnostics Pros & Cons
# Run: manim -pqh scene_s60_diag_pc.py Scene_s60_diag_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s60_diag_pc(LinearRegressionVideo):
    def construct(self):
        self.s60_diag_pc()
