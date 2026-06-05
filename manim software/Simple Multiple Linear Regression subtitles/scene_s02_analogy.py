# -*- coding: utf-8 -*-
# S02 - Real-World Analogy
# Run: manim -pqh scene_s02_analogy.py Scene_s02_analogy
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s02_analogy(LinearRegressionVideo):
    def construct(self):
        self.s02_analogy()
