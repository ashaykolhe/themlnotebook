# -*- coding: utf-8 -*-
# S59 - Cooks Distance
# Run: manim -pqh scene_s59_cooks.py Scene_s59_cooks
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s59_cooks(LinearRegressionVideo):
    def construct(self):
        self.s59_cooks()
