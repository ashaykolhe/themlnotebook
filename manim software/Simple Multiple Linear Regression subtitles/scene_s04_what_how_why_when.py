# -*- coding: utf-8 -*-
# S04 - What / How / Why / When Grid
# Run: manim -pqh scene_s04_what_how_why_when.py Scene_s04_what_how_why_when
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s04_what_how_why_when(LinearRegressionVideo):
    def construct(self):
        self.s04_what_how_why_when()
