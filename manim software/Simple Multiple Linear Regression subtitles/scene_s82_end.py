# -*- coding: utf-8 -*-
# S82 - End Card
# Run: manim -pqh scene_s82_end.py Scene_s82_end
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s82_end(LinearRegressionVideo):
    def construct(self):
        self.s82_end()
