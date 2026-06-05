# -*- coding: utf-8 -*-
# S39 - Adjusted R2
# Run: manim -pqh scene_s39_adj_r2.py Scene_s39_adj_r2
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s39_adj_r2(LinearRegressionVideo):
    def construct(self):
        self.s39_adj_r2()
