# -*- coding: utf-8 -*-
# S38 - R2 Pros & Cons
# Run: manim -pqh scene_s38_r2_pc.py Scene_s38_r2_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s38_r2_pc(LinearRegressionVideo):
    def construct(self):
        self.s38_r2_pc()
