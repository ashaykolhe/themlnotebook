# Polynomial Regression — Complete YouTube Script with Animation Cues
## Data Science Channel | Single Video Production

---

## [ANIM_01] INTRO / TITLE CARD
**Duration:** ~8s
**Subtitle:** "Polynomial Regression — The Complete Guide"
- Title animation with channel branding

---

## [ANIM_02] WHAT IS POLYNOMIAL REGRESSION?
**Duration:** ~20s
**Subtitle:** "What is Polynomial Regression?"

Polynomial regression models the relationship between x and y as an nth-degree polynomial.
It is used when data has a curved, non-linear pattern that a straight line cannot capture.

**Core idea:** Fit a curved line by engineering higher-power features — x², x³ — from the original input, then run ordinary linear regression on those expanded features. Same math, different features.

---

## [ANIM_03] THE FIVE W's — OVERVIEW CARDS
**Duration:** ~25s
**Subtitle:** "What, How, Why, Where, When — The Five W's"

- WHAT: Fits a curved polynomial function (degree ≥ 2) to capture non-linear relationships.
- HOW: Creates [x, x², x³, …, xⁿ] features, then fits a linear model using OLS.
- WHY: Real-world data is rarely linear. Polynomial regression gives curve-fitting power without switching to a new algorithm.
- WHERE: Physics, economics, biology, engineering, climate science.
- WHEN: When scatter plot shows curvature or linear residuals show systematic patterns.
- MECHANISM: Linear in parameters β, but non-linear in x. Solved by Normal Equations.

---

## [ANIM_04] WHY LINEAR REGRESSION FAILS — CHART
**Duration:** ~20s
**Subtitle:** "Why a straight line fails on curved data"

Show scatter plot with a clear curve. Draw a red straight line that misses the curve systematically. Then draw a green quadratic curve that fits the data well. The residuals from the straight line form a U-shape pattern.

---

## [ANIM_05] OVERALL PROS AND CONS
**Duration:** ~20s
**Subtitle:** "Polynomial Regression — Strengths and Weaknesses"

PROS: Captures non-linearity. Reuses OLS. Interpretable coefficients. Flexible degree.
CONS: Overfits easily at high degrees. Extrapolation is catastrophically unreliable. Feature explosion with many inputs. Multicollinearity between polynomial terms.

---

## [ANIM_06] INTUITION — HILLY ROAD ANALOGY
**Duration:** ~18s
**Subtitle:** "Intuition: Like a bendable ruler"

Imagine modelling the elevation of a hilly road. A linear model says the road is a straight ramp — clearly wrong. A polynomial model bends to follow the hills. The degree controls how many hills you can capture.

"Polynomial regression is like giving your model a bendable ruler instead of a rigid straight-edge."

---

## [ANIM_07] FEATURE ENGINEERING INSIGHT
**Duration:** ~18s
**Subtitle:** "The key trick: we never actually solve a non-linear problem"

We never actually solve a non-linear problem. We create new columns from x:
Original: x → Extended: [1, x, x², x³, ..., xⁿ]

Now the relationship between these new columns and y is linear — solved by OLS exactly as before. The curve in the output is a consequence of the curved features we engineered.

---

## [ANIM_08] REAL-WORLD EXAMPLES TABLE
**Duration:** ~20s
**Subtitle:** "Where Polynomial Regression Appears in the Real World"

Table of domains, x variables, y variables, and why polynomial fits:
- Physics: Time → Height of ball (gravity is quadratic)
- Economics: Advertising spend → Revenue (diminishing returns)
- Biology: Age → Height (rapid growth then plateau)
- HR: Years experience → Salary (rises fast then levels off)
- Engineering: Temperature → Material stress
- Chemistry: Concentration → Reaction rate

---

## [ANIM_09] THE POLYNOMIAL EQUATION
**Duration:** ~22s
**Subtitle:** "The Polynomial Equation"

ŷ = β₀ + β₁x + β₂x² + β₃x³ + ... + βₙxⁿ + ε

Term breakdown table:
- ŷ: Predicted value
- β₀: Intercept — value when x = 0
- β₁: Linear coefficient — effect of x
- β₂: Quadratic coefficient — adds 1 bend (parabola)
- β₃: Cubic coefficient — adds up to 2 bends
- βₙ: Degree-n coefficient
- ε: Error term — irreducible noise

KEY RULE: A polynomial of degree n has at most n−1 turning points.

---

## [ANIM_10] DEGREE CONTROLS THE CURVE SHAPE
**Duration:** ~20s
**Subtitle:** "How Degree Controls the Curve Shape"

Show four curves side by side:
- Degree 1: straight line (0 bends)
- Degree 2: parabola (1 bend)
- Degree 3: S-curve (2 bends)
- Degree 4: W-shape (3 bends)

---

## [ANIM_11] WHY IT IS STILL "LINEAR" REGRESSION
**Duration:** ~18s
**Subtitle:** "Why is it STILL called 'Linear' Regression?"

"Linear" means linear in the PARAMETERS β — not linear in x. This is the number one interview trap.

Linear in β: y = β₀ + β₁x + β₂x²  → OLS can solve this exactly.
Non-linear in β: y = β₀ · e^(β₁x) → β₁ is inside an exponent → requires gradient descent.

---

## [ANIM_12] THE NORMAL EQUATIONS
**Duration:** ~18s
**Subtitle:** "The Normal Equations — Optimal Solution in One Step"

After building the design matrix X (columns: 1, x, x², …, xⁿ):

β̂ = (XᵀX)⁻¹ · Xᵀy

Minimises the sum of squared residuals exactly — no iteration needed.

---

## [ANIM_13] NORMAL EQUATIONS PROS AND CONS
**Duration:** ~18s
**Subtitle:** "Normal Equations — Pros and Cons"

PROS: Exact closed-form solution. Globally optimal. No convergence issues. Simple to implement.
CONS: Computing (XᵀX)⁻¹ is O(p³) — expensive for high degrees. Numerically unstable with multicollinearity. Not suitable for very large datasets.

---

## [ANIM_14] COST FUNCTION AND GRADIENT DESCENT
**Duration:** ~18s
**Subtitle:** "Cost Function: MSE and Gradient Descent"

MSE = (1/m) · Σᵢ (yᵢ − ŷᵢ)²

When the dataset is too large for Normal Equations, use gradient descent:
βⱼ := βⱼ − α · (∂MSE/∂βⱼ)  [repeated until convergence]

---

## [ANIM_15] GRADIENT DESCENT PROS AND CONS
**Duration:** ~18s
**Subtitle:** "Gradient Descent — Pros and Cons"

PROS: Scales to large datasets. Works even when XᵀX is not invertible. Memory efficient.
CONS: Requires learning rate tuning. Slower than Normal Equations for small datasets. Convergence not guaranteed without careful tuning (though MSE is convex for polynomial regression).

---

## [ANIM_16] ASSUMPTIONS — LINE-MO FRAMEWORK
**Duration:** ~18s
**Subtitle:** "Assumptions: The LINE-MO Framework"

Polynomial regression inherits all assumptions of linear regression.
L — Linearity in parameters
I — Independence of observations
N — Normality of residuals
E — Equal variance (Homoscedasticity)
M — No severe Multicollinearity
O — No extreme Outliers

---

## [ANIM_17] ASSUMPTION 1 — LINEARITY
**Duration:** ~18s
**Subtitle:** "Assumption 1: Linearity in Parameters"

The relationship between the polynomial features and y must be a linear combination of β.
Detection: Residuals vs fitted values — look for remaining curves.
Remedy: Increase degree; try log/sqrt transformations; switch to non-linear models.

PROS (when satisfied): OLS gives unbiased estimates. Coefficients are meaningful.
CONS (when violated): Systematic residual patterns. Model underfits no matter the degree.

---

## [ANIM_18] ASSUMPTION 2 — INDEPENDENCE
**Duration:** ~16s
**Subtitle:** "Assumption 2: Independence of Observations"

Residuals must be uncorrelated. Violated in time series or spatial data.
Detection: Durbin-Watson statistic (values near 2 = no autocorrelation).
Remedy: Use ARIMA for time series; mixed-effects models for grouped data.

---

## [ANIM_19] ASSUMPTION 3 — NORMALITY
**Duration:** ~16s
**Subtitle:** "Assumption 3: Normality of Residuals"

Residuals should be approximately normal. Only needed for confidence intervals and hypothesis tests.
Detection: Q-Q plot; Shapiro-Wilk test; histogram of residuals.
Remedy: Log-transform y; Box-Cox transformation; remove influential outliers.

---

## [ANIM_20] ASSUMPTION 4 — HOMOSCEDASTICITY
**Duration:** ~16s
**Subtitle:** "Assumption 4: Equal Variance (Homoscedasticity)"

Residual variance must be constant across all fitted values. Funnel shape = heteroscedasticity.
Detection: Residual vs Fitted plot; Breusch-Pagan test.
Remedy: Log-transform y; Weighted Least Squares; robust standard errors.

---

## [ANIM_21] ASSUMPTION 5 — MULTICOLLINEARITY
**Duration:** ~20s
**Subtitle:** "Assumption 5: No Severe Multicollinearity — Critical for Polynomial!"

x, x², x³ are inherently correlated — computed from the same x.
This makes XᵀX nearly singular, causing unstable coefficients.

VIF (Variance Inflation Factor): VIF = 1/(1 − R²ⱼ)
VIF > 5 = moderate; VIF > 10 = severe multicollinearity.

Remedy: Center x before computing powers. Apply Ridge regularisation. Use orthogonal polynomials.

---

## [ANIM_22] ASSUMPTION 5 PROS AND CONS
**Duration:** ~16s
**Subtitle:** "Multicollinearity — Impact on Your Model"

PROS (no multicollinearity): Coefficients are individually interpretable. Standard errors are reliable.
CONS (severe multicollinearity): Numerically unstable coefficients. Tiny data changes cause huge coefficient changes. Model still predicts OK but is uninterpretable.

---

## [ANIM_23] ASSUMPTION 6 — OUTLIERS
**Duration:** ~16s
**Subtitle:** "Assumption 6: No Extreme Outliers or Influential Points"

Outliers are amplified in polynomial regression. One edge point can pull the entire curve wildly.
Detection: Cook's Distance Dᵢ > 4/n; Leverage (hat matrix); standardised residuals > ±3.
Remedy: Robust regression (Huber loss); remove confirmed outliers; winsorise extreme values.

---

## [ANIM_24] BIAS-VARIANCE TRADEOFF
**Duration:** ~22s
**Subtitle:** "The Bias-Variance Tradeoff"

Total Error = Bias² + Variance + Irreducible Noise

Bias²: Systematic error — model too simple — underfitting.
Variance: Predictions fluctuate across different training sets — model too complex — overfitting.
Noise: Irreducible randomness — cannot be reduced by any model.

The polynomial degree is a direct dial on the bias-variance tradeoff.

---

## [ANIM_25] BIAS-VARIANCE CHART
**Duration:** ~20s
**Subtitle:** "Bias and Variance vs. Polynomial Degree"

Chart showing as degree increases: Bias² falls, Variance rises, Total Error has a U-shape minimum at the optimal degree.

---

## [ANIM_26] LOW / OPTIMAL / HIGH DEGREE CARDS
**Duration:** ~20s
**Subtitle:** "Underfitting, Good Fit, and Overfitting"

Low Degree — High Bias: Too rigid. Bad train AND test error. More data won't fix it.
Optimal Degree — Balanced: Fits signal, ignores noise. Good train AND test error.
High Degree — High Variance: Memorises noise. Near-zero train error, high test error.

---

## [ANIM_27] OVERFITTING — DEFINITION AND SIGNS
**Duration:** ~20s
**Subtitle:** "Overfitting — Signs and Causes"

Overfitting: The model learns training data too well — including noise — and fails to generalise.

Signs of overfitting:
- Train R² ≈ 1.0, Test R² much less than 1.0
- Huge coefficient magnitudes (millions)
- Wildly oscillating curve (Runge's phenomenon)
- Test MSE much greater than Train MSE

---

## [ANIM_28] RUNGE'S PHENOMENON
**Duration:** ~18s
**Subtitle:** "Runge's Phenomenon — Oscillation at High Degrees"

Runge (1901): High-degree polynomial interpolation at equally-spaced points oscillates wildly near the edges — even when the true function is perfectly smooth.

The oscillations grow worse as the degree increases.
True function: 1/(1+x²) — smooth everywhere.
High-degree polynomial: explodes near the edges.

---

## [ANIM_29] OVERFITTING PROS AND CONS
**Duration:** ~18s
**Subtitle:** "Fixing and Understanding Overfitting"

FIXES: Reduce polynomial degree. Add regularisation (Ridge/Lasso). Collect more data. Use Lasso for feature selection. Cross-validate degree selection.
WHY IT HAPPENS: n+1 parameters for degree-n polynomial. No built-in penalty in plain OLS. High-degree terms amplify edge effects.

---

## [ANIM_30] UNDERFITTING
**Duration:** ~16s
**Subtitle:** "Underfitting — Too Simple to Capture the Pattern"

Underfitting: Model is too simple to capture the true relationship. High bias.

Signs: Both Train R² and Test R² are low. Residual plot shows systematic curves. Learning curves plateau high.

FIXES: Increase degree. Add more input features. Reduce regularisation. Consider a different model.

---

## [ANIM_31] DEGREE SELECTION — VISUAL INSPECTION
**Duration:** ~16s
**Subtitle:** "Method 1: Visual Inspection — Start Here"

Plot scatter of y vs x. Count how many bends the data seems to have.
One hill → degree 2. S-shape → degree 3.
This gives a starting hypothesis, not a final answer.

PROS: Quick and intuitive. CONS: Subjective with noisy data.

---

## [ANIM_32] DEGREE SELECTION — CROSS-VALIDATION
**Duration:** ~20s
**Subtitle:** "Method 2: K-Fold Cross-Validation — The Gold Standard"

Split data into k folds (k=5 or 10). For each candidate degree: train on k−1 folds, evaluate on the held-out fold, repeat k times, average the error. Pick the degree with the lowest average validation error.

PROS: Uses all data. Low variance estimate. Works for any metric. Can simultaneously tune degree + alpha.
CONS: k× more expensive to compute.

---

## [ANIM_33] DEGREE SELECTION — LEARNING CURVES
**Duration:** ~16s
**Subtitle:** "Method 3: Learning Curves — Diagnose Bias vs Variance"

Plot train error and validation error vs. training set size:
- Both curves plateau high and close → Underfitting → increase degree
- Train low, validation high, large gap → Overfitting → decrease degree or regularise
- Both curves converge low → Good fit

---

## [ANIM_34] DEGREE SELECTION — AIC AND BIC
**Duration:** ~16s
**Subtitle:** "Method 4: AIC and BIC — Statistical Criteria"

AIC = 2k − 2ln(L)
BIC = k·ln(n) − 2ln(L)

k = number of parameters, n = sample size, L = maximised likelihood. Lower = better.
BIC penalises extra parameters more heavily — favours simpler models with large datasets.

---

## [ANIM_35] DEGREE SELECTION — ADJUSTED R²
**Duration:** ~14s
**Subtitle:** "Method 5: Adjusted R² — Quick Check"

Adj-R² = 1 − [(1 − R²)(n−1) / (n−k−1)]

Only increases if the new polynomial term genuinely improves the model.
Decreases when adding a useless term.

---

## [ANIM_36] TRAIN vs VALIDATION ERROR CHART
**Duration:** ~18s
**Subtitle:** "Train vs. Validation Error — Finding the Optimal Degree"

Chart showing classic elbow curve: train error drops monotonically with degree, validation error drops then rises. The optimal degree is where validation error bottoms out.

---

## [ANIM_37] REGULARISATION — OVERVIEW
**Duration:** ~16s
**Subtitle:** "Regularisation — Controlling Model Complexity"

Regularisation adds a penalty on the size of the coefficients to the cost function.
This forces the model to keep coefficients small — producing smoother curves that generalise better.

Three variants: Ridge (L2), Lasso (L1), ElasticNet (L1 + L2 mix).

---

## [ANIM_38] RIDGE REGRESSION
**Duration:** ~18s
**Subtitle:** "Ridge Regression — L2 Regularisation"

Cost = MSE + α · Σⱼ βⱼ²

Ridge shrinks all coefficients toward zero but never exactly to zero.
Acts as a smoothness enforcer — resists extreme oscillations.

PROS: Always has a unique closed-form solution. Works well when all polynomial terms contribute. Reduces multicollinearity impact.
CONS: Cannot zero out coefficients. Still includes all polynomial terms. Biased estimator.

---

## [ANIM_39] LASSO REGRESSION
**Duration:** ~18s
**Subtitle:** "Lasso Regression — L1 Regularisation"

Cost = MSE + α · Σⱼ |βⱼ|

Lasso can set coefficients to exactly zero — performing automatic polynomial term selection.
If your degree-5 polynomial only truly needs degree-3, Lasso will zero out the degree-4 and degree-5 coefficients.

Geometric reason: The L1 constraint region (diamond) has corners on the axes. OLS contours most often hit at a corner — where one or more coefficients are exactly zero.

PROS: Automatic feature selection. Sparse, interpretable models.
CONS: No closed-form solution. Unstable when features are highly correlated.

---

## [ANIM_40] ELASTICNET REGRESSION
**Duration:** ~18s
**Subtitle:** "ElasticNet — The Best Default for Polynomial Regression"

Cost = MSE + α · [ρ·Σ|βⱼ| + (1−ρ)·Σβⱼ²]

ρ (l1_ratio): 0 → pure Ridge. 1 → pure Lasso. 0.5 → equal mix.

PROS: Groups correlated polynomial terms. Can produce sparse solutions. More stable than Lasso for correlated features.
CONS: Two hyperparameters to tune (α and l1_ratio). No closed-form solution.

---

## [ANIM_41] REGULARISATION COMPARISON TABLE
**Duration:** ~18s
**Subtitle:** "Ridge vs. Lasso vs. ElasticNet — Side-by-Side"

Table comparing: coefficient behaviour, feature selection, handling of correlated features, solution type, best use case for polynomial regression.

---

## [ANIM_42] ALPHA HYPERPARAMETER EFFECT
**Duration:** ~16s
**Subtitle:** "The α Hyperparameter — Controlling Regularisation Strength"

α = 0: No regularisation → plain OLS → can overfit.
Small α (0.001–0.1): Mild penalty → slight coefficient shrinkage.
Moderate α (1–10): Strong shrinkage → much smoother polynomial.
Very large α (100+): Over-regularisation → coefficients approach 0 → underfitting.

---

## [ANIM_43] FEATURE SCALING
**Duration:** ~16s
**Subtitle:** "Feature Scaling — Why It Matters"

When you compute polynomial features, x² can be in the millions while x is in the hundreds. This massive scale difference causes serious problems for regularisation and gradient descent.

Correct pipeline order: Raw x → PolynomialFeatures → StandardScaler → Model

---

## [ANIM_44] STANDARD SCALER
**Duration:** ~16s
**Subtitle:** "StandardScaler — Z-score Normalisation"

x_scaled = (x − μ) / σ

Transforms each feature to mean=0 and std=1.
Fit on train only. Transform both train and test with the same scaler.

PROS: Makes regularisation fair. Prevents numerical instability. Speeds up gradient descent.
CONS: Sensitive to outliers. Coefficients in standardised units — harder to interpret.

---

## [ANIM_45] MINMAX SCALER PROS AND CONS
**Duration:** ~14s
**Subtitle:** "MinMaxScaler vs StandardScaler"

MinMax: x_scaled = (x − x_min) / (x_max − x_min) → scales to [0, 1]

PROS: Preserves zero values.
CONS: Very sensitive to outliers. For polynomial regression, StandardScaler is almost always preferred.

---

## [ANIM_46] WHY CENTERING REDUCES MULTICOLLINEARITY
**Duration:** ~14s
**Subtitle:** "Centering x Reduces Multicollinearity Between Powers"

If x ranges from 10 to 20, then x and x² are highly correlated (cor ≈ 0.99).
If you center first (x − 15), x ranges from −5 to 5. The correlation between (x−15) and (x−15)² drops dramatically.

---

## [ANIM_47] FEATURE EXPLOSION
**Duration:** ~18s
**Subtitle:** "Feature Explosion — The Curse of Dimensionality"

Number of features after expansion = C(n + d, d) = (n + d)! / (n! · d!)

n = original features, d = degree. Grows explosively.

Table: 1 feature degree 2 → 3 features. 10 features degree 3 → 286 features. 100 features degree 3 → 176,851 features!

---

## [ANIM_48] FEATURE EXPLOSION PROS AND CONS
**Duration:** ~16s
**Subtitle:** "Feature Explosion — When to Use and When to Avoid"

USE WHEN: Small number of original features (≤ 5). Low degree (2–3). Large enough dataset. Regularisation applied.
AVOID WHEN: Many original features (n > 10). High degree (> 3). Small dataset. Consider kernel SVR instead.

The Kernel Trick: SVR with polynomial kernel computes polynomial features implicitly — without materialising them. Avoids the memory cost of feature explosion.

---

## [ANIM_49] EVALUATION METRICS — MSE AND RMSE
**Duration:** ~18s
**Subtitle:** "Evaluation Metrics — MSE and RMSE"

MSE = (1/n) · Σ (yᵢ − ŷᵢ)²  |  Units: y²  |  Range: [0, ∞)
RMSE = √MSE  |  Same units as y  |  Most interpretable error metric

MSE PROS: Differentiable. Penalises large errors heavily. Convex.
MSE CONS: Not in same units as y. Sensitive to outliers.
RMSE: "On average, our predictions are off by ±RMSE units."

---

## [ANIM_50] EVALUATION METRICS — MAE AND R²
**Duration:** ~18s
**Subtitle:** "Evaluation Metrics — MAE and R²"

MAE = (1/n) · Σ |yᵢ − ŷᵢ|  |  Range: [0, ∞)  |  Same units as y
R² = 1 − SS_res / SS_tot  |  Range: (−∞, 1]

MAE: Robust to outliers. Intuitive: average absolute mistake.
R² WARNING: Adding more polynomial terms ALWAYS increases training R². Never use it alone to select degree!

---

## [ANIM_51] ADJUSTED R² AND MAPE
**Duration:** ~16s
**Subtitle:** "Adjusted R² and MAPE"

Adj-R² = 1 − [(1−R²)(n−1) / (n−k−1)]  — penalises complexity. Better than R² for degree comparison.

MAPE = (100/n) · Σ |yᵢ − ŷᵢ| / |yᵢ|  — expressed as a percentage.
MAPE CONS: Undefined when yᵢ = 0. Asymmetric penalty for over vs under prediction.

---

## [ANIM_52] CONFIDENCE AND PREDICTION INTERVALS
**Duration:** ~20s
**Subtitle:** "Confidence Intervals vs. Prediction Intervals"

CI (for the mean response): ŷ₀ ± t · σ̂ · √(x₀ᵀ(XᵀX)⁻¹x₀)
→ "What range contains the AVERAGE y at x₀?"

PI (for a new individual): ŷ₀ ± t · σ̂ · √(1 + x₀ᵀ(XᵀX)⁻¹x₀)
→ "What range will contain ONE NEW observation's y at x₀?"

PI is ALWAYS wider than CI because it adds irreducible individual variance (the +1 inside the square root).

---

## [ANIM_53] SKLEARN PIPELINE
**Duration:** ~20s
**Subtitle:** "The Correct scikit-learn Pipeline"

Pipeline steps: Raw x → PolynomialFeatures(degree=d) → StandardScaler → Ridge/Lasso/ElasticNet

Key parameters shown: degree, include_bias=False, alpha, fit on train only.

GridSearchCV tunes degree and alpha simultaneously with 5-fold cross-validation.

---

## [ANIM_54] HYPERPARAMETERS — POLYNOMIAL FEATURES
**Duration:** ~18s
**Subtitle:** "PolynomialFeatures Hyperparameters"

degree (default=2): Maximum polynomial degree. Use 2–5 for most problems. Select via GridSearchCV.
include_bias (default=True): Set to False when downstream model has fit_intercept=True.
interaction_only (default=False): If True, only cross-product terms (x₁·x₂), not pure polynomial terms.
order (default='C'): Memory layout. Leave as 'C' unless you have a specific performance reason.

---

## [ANIM_55] HYPERPARAMETERS — RIDGE
**Duration:** ~18s
**Subtitle:** "Ridge Hyperparameters"

alpha (default=1.0): Regularisation strength. MOST IMPORTANT. Search log-spaced: [0.001, 0.01, 0.1, 1, 10, 100, 1000].
solver (default='auto'): 'svd' for numerical stability; 'sag'/'saga' for very large datasets.
tol (default=1e-4): Convergence tolerance for iterative solvers.
max_iter (default=None): Maximum iterations for iterative solvers.

---

## [ANIM_56] HYPERPARAMETERS — LASSO AND ELASTICNET
**Duration:** ~18s
**Subtitle:** "Lasso and ElasticNet Hyperparameters"

Lasso: alpha, max_iter (set to 10000+ for high-degree polynomial), tol, warm_start, selection.
ElasticNet: alpha (overall strength), l1_ratio (0=Ridge, 1=Lasso, 0.5=equal mix).
Recommended l1_ratio search: [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 1.0].

---

## [ANIM_57] OVERALL PROS AND CONS — DETAILED
**Duration:** ~22s
**Subtitle:** "Overall Pros and Cons of Polynomial Regression"

PROS (10): Captures non-linearity. No new algorithm needed. Interpretable. Exact closed-form. Flexible degree. Works with small datasets. Probabilistic (CI/PI). Combines well with regularisation. Prediction intervals. Feature engineering insight.

CONS (9): Overfits easily. Catastrophic extrapolation. Feature explosion. Multicollinearity. Degree selection is hard. Sensitive to outliers. Computational cost O(p³). Runge's phenomenon. Not competitive for complex patterns.

---

## [ANIM_58] WHEN TO USE POLYNOMIAL REGRESSION
**Duration:** ~18s
**Subtitle:** "When to Use Polynomial Regression"

USE WHEN: Scatter plot shows clear curvature. Domain theory implies polynomial form. Linear residuals show systematic curves. Interpretability required. Small number of features (≤ 5). Degree ≤ 3–4 sufficient. Data stays within training range.

DON'T USE WHEN: Need extrapolation. Many input features (≥ 10). Truly non-polynomial relationship. Very large dataset. Curvature is localised (use spline regression). Maximum predictive accuracy required.

---

## [ANIM_59] ALTERNATIVES COMPARISON TABLE
**Duration:** ~18s
**Subtitle:** "Polynomial Regression vs. Alternatives"

Table: Spline Regression (local curvature), Decision Tree (complex patterns), Random Forest/XGBoost (high accuracy, large datasets), SVR polynomial kernel (high-dimensional, kernel trick), Neural Network (very complex patterns), Log/Box-Cox + Linear (multiplicative relationships), LOESS (non-parametric smoothing).

---

## [ANIM_60] COMMON MISTAKES TABLE
**Duration:** ~20s
**Subtitle:** "10 Common Mistakes — And How to Fix Them"

Table of 10 mistakes: Using training R² to select degree. Scaling before polynomial expansion. Fitting scaler on test data (data leakage). Extrapolating beyond training range. High degree without regularisation. Interpreting individual coefficients at high degree. Not checking residual plots. include_bias=True with fit_intercept=True. Too few max_iter for Lasso. Not using Pipeline.

---

## [ANIM_61] INTERVIEW Q&A — IS IT LINEAR?
**Duration:** ~18s
**Subtitle:** "Interview Q: Is Polynomial Regression Linear or Non-Linear?"

Answer: It IS a linear model — linear in its parameters β.
"Linear" means a linear combination of parameters, not linear in x.
y = β₀ + β₁x + β₂x² is still a linear combination of β₀, β₁, β₂.
OLS solves it with the same Normal Equations as linear regression.

---

## [ANIM_62] INTERVIEW Q&A — OVERFITTING
**Duration:** ~18s
**Subtitle:** "Interview Q: Why Does Polynomial Regression Overfit So Easily?"

Three reasons: (1) More parameters — degree-n has n+1 coefficients. (2) No built-in penalty — OLS minimises training error with zero concern for coefficient magnitude. (3) Runge's phenomenon — at degree n-1 for n data points, the polynomial passes through EVERY point with R² = 1.0.

---

## [ANIM_63] INTERVIEW Q&A — TRAIN 0.99 TEST 0.3
**Duration:** ~18s
**Subtitle:** "Interview Q: Train R²=0.99, Test R²=0.3. What Happened?"

Classic overfitting. Model memorised training noise. Very low bias, extremely high variance.
Fixes: Reduce degree via cross-validation. Add Ridge or Lasso. Get more training data. Use Lasso to zero out unnecessary terms.

---

## [ANIM_64] INTERVIEW Q&A — SCALE AFTER POLY
**Duration:** ~16s
**Subtitle:** "Interview Q: Why Scale AFTER Polynomial Expansion?"

StandardScaler needs to see the actual distribution of each polynomial feature (x², x³) to compute their correct mean and std. If you scale x first, the polynomial features are derived from already-scaled x — their statistics are different. With regularisation, the penalty must treat all features fairly — possible only if they're on consistent scales.

---

## [ANIM_65] INTERVIEW Q&A — WHY LASSO PRODUCES ZEROS
**Duration:** ~16s
**Subtitle:** "Interview Q: Why Does Lasso Produce Sparse Solutions?"

Geometric explanation: Ridge constraint region = sphere (no corners). Lasso constraint region = diamond (corners on the axes). OLS contours most often intersect the diamond at a corner — where one or more coefficients are exactly zero. Ridge has no corners, so the intersection is never exactly zero.

---

## [ANIM_66] OUTRO / SUMMARY
**Duration:** ~12s
**Subtitle:** "Polynomial Regression — Summary"

Key takeaways: It's linear in parameters. Degree controls bias-variance tradeoff. Always scale AFTER polynomial expansion. Use Ridge/Lasso/ElasticNet for regularisation. Select degree via cross-validation. Never extrapolate. Use Pipeline in scikit-learn.

---

*End of YouTube Script*
*Total estimated video duration: ~20–25 minutes*
