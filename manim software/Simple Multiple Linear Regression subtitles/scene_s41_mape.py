# -*- coding: utf-8 -*-
# S41 - MAPE Formula
# Run: manim -pqh scene_s41_mape.py Scene_s41_mape
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s41_mape(LinearRegressionVideo):
    def construct(self):
        self.s41_mape()
