# -*- coding: utf-8 -*-
# S71 - CV Pros & Cons
# Run: manim -pqh scene_s71_cv_pc.py Scene_s71_cv_pc
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s71_cv_pc(LinearRegressionVideo):
    def construct(self):
        self.s71_cv_pc()
