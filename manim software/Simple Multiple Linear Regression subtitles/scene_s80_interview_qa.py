# -*- coding: utf-8 -*-
# S80 - Interview QA Highlights
# Run: manim -pqh scene_s80_interview_qa.py Scene_s80_interview_qa
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s80_interview_qa(LinearRegressionVideo):
    def construct(self):
        self.s80_interview_qa()
