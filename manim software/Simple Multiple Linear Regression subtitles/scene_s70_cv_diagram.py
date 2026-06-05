# -*- coding: utf-8 -*-
# S70 - 5-Fold CV Diagram
# Run: manim -pqh scene_s70_cv_diagram.py Scene_s70_cv_diagram
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s70_cv_diagram(LinearRegressionVideo):
    def construct(self):
        self.s70_cv_diagram()
