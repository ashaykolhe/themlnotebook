# -*- coding: utf-8 -*-
# S16 - LINE-MO Assumptions Overview
# Run: manim -pqh scene_s16_linemo_overview.py Scene_s16_linemo_overview
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s16_linemo_overview(LinearRegressionVideo):
    def construct(self):
        self.s16_linemo_overview()
