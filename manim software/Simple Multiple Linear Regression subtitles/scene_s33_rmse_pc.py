# -*- coding: utf-8 -*-
# S33 - RMSE Pros & Cons
# Run: manim -pqh scene_s33_rmse_pc.py Scene_s33_rmse_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s33_rmse_pc(LinearRegressionVideo):
    def construct(self):
        self.s33_rmse_pc()
