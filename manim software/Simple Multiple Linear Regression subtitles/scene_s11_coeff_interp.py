# -*- coding: utf-8 -*-
# S11 - Coefficient Interpretation
# Run: manim -pqh scene_s11_coeff_interp.py Scene_s11_coeff_interp
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s11_coeff_interp(LinearRegressionVideo):
    def construct(self):
        self.s11_coeff_interp()
