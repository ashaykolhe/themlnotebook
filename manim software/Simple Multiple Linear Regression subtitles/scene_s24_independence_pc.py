# -*- coding: utf-8 -*-
# S24 - Independence Pros & Cons
# Run: manim -pqh scene_s24_independence_pc.py Scene_s24_independence_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s24_independence_pc(LinearRegressionVideo):
    def construct(self):
        self.s24_independence_pc()
