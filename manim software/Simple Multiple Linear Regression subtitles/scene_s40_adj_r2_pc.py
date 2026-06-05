# -*- coding: utf-8 -*-
# S40 - Adjusted R2 Pros & Cons
# Run: manim -pqh scene_s40_adj_r2_pc.py Scene_s40_adj_r2_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s40_adj_r2_pc(LinearRegressionVideo):
    def construct(self):
        self.s40_adj_r2_pc()
