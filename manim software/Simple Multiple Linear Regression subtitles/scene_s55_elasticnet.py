# -*- coding: utf-8 -*-
# S55 - ElasticNet
# Run: manim -pqh scene_s55_elasticnet.py Scene_s55_elasticnet
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_s55_elasticnet(LinearRegressionVideo):
    def construct(self):
        self.s55_elasticnet()
