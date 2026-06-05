# -*- coding: utf-8 -*-
# S47 - GD Types Table
# Run: manim -pqh scene_s47_gd_types.py Scene_s47_gd_types
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s47_gd_types(LinearRegressionVideo):
    def construct(self):
        self.s47_gd_types()
