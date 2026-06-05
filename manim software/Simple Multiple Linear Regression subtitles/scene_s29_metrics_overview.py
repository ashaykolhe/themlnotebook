# -*- coding: utf-8 -*-
# S29 - Evaluation Metrics Overview
# Run: manim -pqh scene_s29_metrics_overview.py Scene_s29_metrics_overview
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s29_metrics_overview(LinearRegressionVideo):
    def construct(self):
        self.s29_metrics_overview()
