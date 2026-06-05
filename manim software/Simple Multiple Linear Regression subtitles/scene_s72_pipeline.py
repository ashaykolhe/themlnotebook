# -*- coding: utf-8 -*-
# S72 - Pipelines and Data Leakage
# Run: manim -pqh scene_s72_pipeline.py Scene_s72_pipeline
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s72_pipeline(LinearRegressionVideo):
    def construct(self):
        self.s72_pipeline()
