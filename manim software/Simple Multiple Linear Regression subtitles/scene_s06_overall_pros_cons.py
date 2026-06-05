# -*- coding: utf-8 -*-
# S06 - Overall Pros & Cons
# Run: manim -pqh scene_s06_overall_pros_cons.py Scene_s06_overall_pros_cons
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s06_overall_pros_cons(LinearRegressionVideo):
    def construct(self):
        self.s06_overall_pros_cons()
