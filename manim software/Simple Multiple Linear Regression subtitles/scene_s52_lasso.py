# -*- coding: utf-8 -*-
# S52 - Lasso Cost Function
# Run: manim -pqh scene_s52_lasso.py Scene_s52_lasso
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s52_lasso(LinearRegressionVideo):
    def construct(self):
        self.s52_lasso()
