# -*- coding: utf-8 -*-
# S78 - When to Use Decision Table
# Run: manim -pqh scene_s78_when_to_use.py Scene_s78_when_to_use
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s78_when_to_use(LinearRegressionVideo):
    def construct(self):
        self.s78_when_to_use()
