# -*- coding: utf-8 -*-
# S61 - Feature Engineering Transforms
# Run: manim -pqh scene_s61_feat_eng.py Scene_s61_feat_eng
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s61_feat_eng(LinearRegressionVideo):
    def construct(self):
        self.s61_feat_eng()
