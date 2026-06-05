# -*- coding: utf-8 -*-
# S01 - Title Card
# Run: manim -pqh scene_s01_title.py Scene_s01_title
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s01_title(LinearRegressionVideo):
    def construct(self):
        self.s01_title()
