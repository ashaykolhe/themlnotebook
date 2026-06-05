# -*- coding: utf-8 -*-
# S63 - Encoding Categorical Features
# Run: manim -pqh scene_s63_encoding.py Scene_s63_encoding
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s63_encoding(LinearRegressionVideo):
    def construct(self):
        self.s63_encoding()
