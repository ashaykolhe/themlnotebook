# -*- coding: utf-8 -*-
# S51 - Ridge Pros & Cons
# Run: manim -pqh scene_s51_ridge_pc.py Scene_s51_ridge_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s51_ridge_pc(LinearRegressionVideo):
    def construct(self):
        self.s51_ridge_pc()
