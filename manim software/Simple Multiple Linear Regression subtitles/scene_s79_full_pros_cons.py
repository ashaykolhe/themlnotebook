# -*- coding: utf-8 -*-
# S79 - Full Overall Pros and Cons
# Run: manim -pqh scene_s79_full_pros_cons.py Scene_s79_full_pros_cons
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s79_full_pros_cons(LinearRegressionVideo):
    def construct(self):
        self.s79_full_pros_cons()
