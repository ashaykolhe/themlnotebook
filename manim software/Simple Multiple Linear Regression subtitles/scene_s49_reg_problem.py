# -*- coding: utf-8 -*-
# S49 - Regularisation The Problem
# Run: manim -pqh scene_s49_reg_problem.py Scene_s49_reg_problem
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s49_reg_problem(LinearRegressionVideo):
    def construct(self):
        self.s49_reg_problem()
