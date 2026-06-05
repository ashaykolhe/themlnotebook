# -*- coding: utf-8 -*-
# S37 - R2 Interpretation Table
# Run: manim -pqh scene_s37_r2_table.py Scene_s37_r2_table
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s37_r2_table(LinearRegressionVideo):
    def construct(self):
        self.s37_r2_table()
