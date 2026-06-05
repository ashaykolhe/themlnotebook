"""
per_scene_classes.py
Per-scene wrapper classes for individual rendering.
Place in the SAME folder as polynomial_regression_video.py

HOW IT WORKS:
Each class inherits PolynomialRegressionVideo so self is a
fully initialised Scene with all helpers available.
construct() overrides the parent and calls ONLY one scene method.
No camera/renderer/property issues.
"""

from polynomial_regression_video import PolynomialRegressionVideo, BG


class Scene01Intro(PolynomialRegressionVideo):
    """Renders only: scene_01_intro"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_01_intro()

class Scene02WhatIs(PolynomialRegressionVideo):
    """Renders only: scene_02_what_is"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_02_what_is()

class Scene03FiveWs(PolynomialRegressionVideo):
    """Renders only: scene_03_five_ws"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_03_five_ws()

class Scene04WhyLinearFails(PolynomialRegressionVideo):
    """Renders only: scene_04_why_linear_fails"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_04_why_linear_fails()

class Scene05OverallProsCons(PolynomialRegressionVideo):
    """Renders only: scene_05_overall_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_05_overall_pros_cons()

class Scene06HillyRoad(PolynomialRegressionVideo):
    """Renders only: scene_06_hilly_road"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_06_hilly_road()

class Scene07FeatureEngineering(PolynomialRegressionVideo):
    """Renders only: scene_07_feature_engineering"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_07_feature_engineering()

class Scene08RealWorld(PolynomialRegressionVideo):
    """Renders only: scene_08_real_world"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_08_real_world()

class Scene09Equation(PolynomialRegressionVideo):
    """Renders only: scene_09_equation"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_09_equation()

class Scene10DegreeShapes(PolynomialRegressionVideo):
    """Renders only: scene_10_degree_shapes"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_10_degree_shapes()

class Scene11WhyLinear(PolynomialRegressionVideo):
    """Renders only: scene_11_why_linear"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_11_why_linear()

class Scene12NormalEquations(PolynomialRegressionVideo):
    """Renders only: scene_12_normal_equations"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_12_normal_equations()

class Scene13NormalEqProsCons(PolynomialRegressionVideo):
    """Renders only: scene_13_normal_eq_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_13_normal_eq_pros_cons()

class Scene14CostGd(PolynomialRegressionVideo):
    """Renders only: scene_14_cost_gd"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_14_cost_gd()

class Scene15GdProsCons(PolynomialRegressionVideo):
    """Renders only: scene_15_gd_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_15_gd_pros_cons()

class Scene16AssumptionsLinemo(PolynomialRegressionVideo):
    """Renders only: scene_16_assumptions_linemo"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_16_assumptions_linemo()

class Scene17AssumptionLinearity(PolynomialRegressionVideo):
    """Renders only: scene_17_assumption_linearity"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_17_assumption_linearity()

class Scene18AssumptionIndependence(PolynomialRegressionVideo):
    """Renders only: scene_18_assumption_independence"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_18_assumption_independence()

class Scene19AssumptionNormality(PolynomialRegressionVideo):
    """Renders only: scene_19_assumption_normality"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_19_assumption_normality()

class Scene20AssumptionHomoscedasticity(PolynomialRegressionVideo):
    """Renders only: scene_20_assumption_homoscedasticity"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_20_assumption_homoscedasticity()

class Scene21AssumptionMulticollinearity(PolynomialRegressionVideo):
    """Renders only: scene_21_assumption_multicollinearity"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_21_assumption_multicollinearity()

class Scene22MulticollinearityProsCons(PolynomialRegressionVideo):
    """Renders only: scene_22_multicollinearity_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_22_multicollinearity_pros_cons()

class Scene23AssumptionOutliers(PolynomialRegressionVideo):
    """Renders only: scene_23_assumption_outliers"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_23_assumption_outliers()

class Scene24BiasVariance(PolynomialRegressionVideo):
    """Renders only: scene_24_bias_variance"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_24_bias_variance()

class Scene25BvChart(PolynomialRegressionVideo):
    """Renders only: scene_25_bv_chart"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_25_bv_chart()

class Scene26FittingCards(PolynomialRegressionVideo):
    """Renders only: scene_26_fitting_cards"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_26_fitting_cards()

class Scene27Overfitting(PolynomialRegressionVideo):
    """Renders only: scene_27_overfitting"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_27_overfitting()

class Scene28Runge(PolynomialRegressionVideo):
    """Renders only: scene_28_runge"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_28_runge()

class Scene29OverfittingProsCons(PolynomialRegressionVideo):
    """Renders only: scene_29_overfitting_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_29_overfitting_pros_cons()

class Scene30Underfitting(PolynomialRegressionVideo):
    """Renders only: scene_30_underfitting"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_30_underfitting()

class Scene31VisualInspection(PolynomialRegressionVideo):
    """Renders only: scene_31_visual_inspection"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_31_visual_inspection()

class Scene32CrossValidation(PolynomialRegressionVideo):
    """Renders only: scene_32_cross_validation"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_32_cross_validation()

class Scene33LearningCurves(PolynomialRegressionVideo):
    """Renders only: scene_33_learning_curves"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_33_learning_curves()

class Scene34AicBic(PolynomialRegressionVideo):
    """Renders only: scene_34_aic_bic"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_34_aic_bic()

class Scene35AdjustedR2(PolynomialRegressionVideo):
    """Renders only: scene_35_adjusted_r2"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_35_adjusted_r2()

class Scene36ErrorCurve(PolynomialRegressionVideo):
    """Renders only: scene_36_error_curve"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_36_error_curve()

class Scene37RegularisationOverview(PolynomialRegressionVideo):
    """Renders only: scene_37_regularisation_overview"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_37_regularisation_overview()

class Scene38Ridge(PolynomialRegressionVideo):
    """Renders only: scene_38_ridge"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_38_ridge()

class Scene39Lasso(PolynomialRegressionVideo):
    """Renders only: scene_39_lasso"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_39_lasso()

class Scene40Elasticnet(PolynomialRegressionVideo):
    """Renders only: scene_40_elasticnet"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_40_elasticnet()

class Scene41RegComparison(PolynomialRegressionVideo):
    """Renders only: scene_41_reg_comparison"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_41_reg_comparison()

class Scene42AlphaEffect(PolynomialRegressionVideo):
    """Renders only: scene_42_alpha_effect"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_42_alpha_effect()

class Scene43FeatureScaling(PolynomialRegressionVideo):
    """Renders only: scene_43_feature_scaling"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_43_feature_scaling()

class Scene44StandardScaler(PolynomialRegressionVideo):
    """Renders only: scene_44_standard_scaler"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_44_standard_scaler()

class Scene45Minmax(PolynomialRegressionVideo):
    """Renders only: scene_45_minmax"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_45_minmax()

class Scene46Centering(PolynomialRegressionVideo):
    """Renders only: scene_46_centering"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_46_centering()

class Scene47FeatureExplosion(PolynomialRegressionVideo):
    """Renders only: scene_47_feature_explosion"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_47_feature_explosion()

class Scene48ExplosionProsCons(PolynomialRegressionVideo):
    """Renders only: scene_48_explosion_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_48_explosion_pros_cons()

class Scene49MseRmse(PolynomialRegressionVideo):
    """Renders only: scene_49_mse_rmse"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_49_mse_rmse()

class Scene50MaeR2(PolynomialRegressionVideo):
    """Renders only: scene_50_mae_r2"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_50_mae_r2()

class Scene51AdjR2Mape(PolynomialRegressionVideo):
    """Renders only: scene_51_adj_r2_mape"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_51_adj_r2_mape()

class Scene52CiPi(PolynomialRegressionVideo):
    """Renders only: scene_52_ci_pi"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_52_ci_pi()

class Scene53Pipeline(PolynomialRegressionVideo):
    """Renders only: scene_53_pipeline"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_53_pipeline()

class Scene54HpPoly(PolynomialRegressionVideo):
    """Renders only: scene_54_hp_poly"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_54_hp_poly()

class Scene55HpRidge(PolynomialRegressionVideo):
    """Renders only: scene_55_hp_ridge"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_55_hp_ridge()

class Scene56HpLassoEnet(PolynomialRegressionVideo):
    """Renders only: scene_56_hp_lasso_enet"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_56_hp_lasso_enet()

class Scene57OverallProsCons(PolynomialRegressionVideo):
    """Renders only: scene_57_overall_pros_cons"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_57_overall_pros_cons()

class Scene58WhenToUse(PolynomialRegressionVideo):
    """Renders only: scene_58_when_to_use"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_58_when_to_use()

class Scene59Alternatives(PolynomialRegressionVideo):
    """Renders only: scene_59_alternatives"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_59_alternatives()

class Scene60Mistakes(PolynomialRegressionVideo):
    """Renders only: scene_60_mistakes"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_60_mistakes()

class Scene61IqLinear(PolynomialRegressionVideo):
    """Renders only: scene_61_iq_linear"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_61_iq_linear()

class Scene62IqOverfit(PolynomialRegressionVideo):
    """Renders only: scene_62_iq_overfit"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_62_iq_overfit()

class Scene63IqTrainTest(PolynomialRegressionVideo):
    """Renders only: scene_63_iq_train_test"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_63_iq_train_test()

class Scene64IqScale(PolynomialRegressionVideo):
    """Renders only: scene_64_iq_scale"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_64_iq_scale()

class Scene65IqLassoZeros(PolynomialRegressionVideo):
    """Renders only: scene_65_iq_lasso_zeros"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_65_iq_lasso_zeros()

class Scene66Outro(PolynomialRegressionVideo):
    """Renders only: scene_66_outro"""
    def construct(self):
        self.camera.background_color = BG
        self.scene_66_outro()
