# -*- coding: utf-8 -*-
# S81 - Master Summary
# Run: manim -pqh scene_s81_summary.py Scene_s81_summary
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s81_summary(LinearRegressionVideo):
    def construct(self):
        self.s81_summary()
