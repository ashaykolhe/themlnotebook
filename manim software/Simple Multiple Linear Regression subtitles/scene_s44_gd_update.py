# -*- coding: utf-8 -*-
# S44 - Gradient Descent Update Rule
# Run: manim -pqh scene_s44_gd_update.py Scene_s44_gd_update
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s44_gd_update(LinearRegressionVideo):
    def construct(self):
        self.s44_gd_update()
