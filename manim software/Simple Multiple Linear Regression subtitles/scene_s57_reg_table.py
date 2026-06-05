# -*- coding: utf-8 -*-
# S57 - Regularisation Comparison Table
# Run: manim -pqh scene_s57_reg_table.py Scene_s57_reg_table
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s57_reg_table(LinearRegressionVideo):
    def construct(self):
        self.s57_reg_table()
