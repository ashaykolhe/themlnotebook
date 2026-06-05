# -*- coding: utf-8 -*-
# S05 - Simple vs Multiple Table
# Run: manim -pqh scene_s05_simple_vs_multiple.py Scene_s05_simple_vs_multiple
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s05_simple_vs_multiple(LinearRegressionVideo):
    def construct(self):
        self.s05_simple_vs_multiple()
