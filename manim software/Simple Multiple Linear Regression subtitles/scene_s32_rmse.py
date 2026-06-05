# -*- coding: utf-8 -*-
# S32 - RMSE Formula
# Run: manim -pqh scene_s32_rmse.py Scene_s32_rmse
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s32_rmse(LinearRegressionVideo):
    def construct(self):
        self.s32_rmse()
