# Text Animation Placement Guide
## Where Every HTML Text Element Goes in the Video

This guide tells you exactly which text from the HTML to animate, 
what animation style to use, and precisely where it fits relative 
to your existing 44 Anim scenes — without disrupting them.

---

## PHILOSOPHY: THREE TIERS OF TEXT

**Tier 1 — Animate it:** Key definitions, formulas, comparisons, warnings.
  These go ON SCREEN as animated text while voiceover explains them.

**Tier 2 — Skip it:** Pros/cons lists, hyperparameter tables, code sections,
  interview Q&As. Too detailed for a video. Put a link in the description instead.

**Tier 3 — Spoken only:** Background context, transitions, the "why" explanations.
  Voiceover handles these. No on-screen text needed.

The rule: if a viewer would pause the video to read it carefully, animate it.
If they'd skim it or need 30 seconds to absorb it, skip it.

---

## ANIMATION STYLES TO USE (all simple Manim)

**TypewriterReveal** — Text types out character by character. Use for single 
  key statements or definitions. Feels like the idea is being "written" live.

**BulletReveal** — Bullet points appear one at a time with a small slide-in.
  Use for short lists of 3–5 items. Each bullet waits 1–2 seconds before the next.

**CardFlip** — A coloured card rectangle fades in, then text appears inside it.
  Matches the HTML card design. Use for warnings and key insight boxes.

**TableBuild** — Table rows animate in one by one from top to bottom.
  Use for comparison tables (2–4 columns max on screen).

**HighlightPop** — A word or phrase is already on screen, then a coloured 
  rectangle appears behind it to highlight it. Use for emphasis mid-explanation.

**SplitReveal** — Screen splits into two panels, content appears in each.
  Already used in LINE-MO anims. Reuse this style for comparisons.

---

## PART 1 — THE HOOK (Anims 01–03, timestamps 0:00–0:45)

### TEXT-A: What/How/Why cards  ← INSERT BETWEEN Anim02 and Anim03
**Style:** CardFlip — 3 cards appear in sequence
**Content from HTML:**
  Card 1 (Blue): WHAT — "Finds the best-fit line between features (X) and 
    a continuous target (y). Uses that line to predict on unseen data."
  Card 2 (Green): HOW — "Minimises the sum of squared differences between 
    actual y and predicted ŷ. Solved analytically (Normal Eq) or iteratively (GD)."
  Card 3 (Orange): WHY USE IT — "Interpretable, blazing fast, no hyperparameters. 
    The mandatory baseline before trying any complex model."
**Duration:** ~8 seconds (cards appear then fade as Anim03 begins)
**Why here:** Viewer just saw use cases flash by. Before the line draws, 
  give them the one-sentence answer to "what is this thing."

### TEXT-B: Simple vs Multiple comparison  ← INSERT AFTER Anim03
**Style:** TableBuild — 2 rows, 3 columns
**Content:**
  | Type     | Features | Geometry          |
  | Simple   | 1        | Line in 2D        |
  | Multiple | 2+       | Hyperplane in N-D |
**Duration:** ~6 seconds
**Why here:** The orange line just drew through 2D data. Naturally prompt: 
  "but what about more features?" This table answers it in 6 seconds.

---

## PART 2 — WHAT IS LINEAR REGRESSION (Anims 04–07, 0:45–2:30)

### TEXT-C: Residual definition box  ← INSERT BETWEEN Anim06 and Anim07
**Style:** CardFlip (Yellow border)
**Content:** "Residual = Actual y − Predicted ŷ
  The model optimises β to make these as small as possible.
  ε in the true model = population equivalent of the sample residual."
**Duration:** ~7 seconds
**Why here:** Residual dashes just appeared (Anim06). Before they shrink (Anim07),
  define the term precisely. Viewer sees the visual + definition simultaneously.

---

## PART 3 — THE EQUATION (Anims 08–12, 2:30–4:30)

### TEXT-D: Symbol table  ← INSERT BETWEEN Anim10 and Anim11
**Style:** TableBuild — 4 rows
**Content:**
  | Symbol  | Name                   | Meaning                              |
  | ŷ       | y-hat (predicted)      | Model output — our best guess        |
  | β₀      | Intercept / bias       | ŷ when all features = 0              |
  | β₁…βₙ  | Coefficients / slopes  | Change in ŷ per 1-unit rise in xᵢ   |
  | x₁…xₙ  | Features / predictors  | The inputs                           |
**Duration:** ~10 seconds (rows appear one by one)
**Why here:** Anim10 just highlighted all coefficient terms. The table 
  locks in the full vocabulary before the concrete example (Anim11).

### TEXT-E: Coefficient scaling warning  ← INSERT AFTER Anim11
**Style:** CardFlip (Yellow/warning border)
**Content:** "⚠ Coefficients ≠ Feature Importance (if features unscaled)
  β = 0.01 for income (dollars) vs β = 2.5 for rooms
  doesn't mean rooms matter 250× more.
  → Always standardise features before comparing coefficients."
**Duration:** ~8 seconds
**Why here:** β₁ = 150 example just appeared. Immediately flag the trap 
  that almost every beginner falls into. Anim12 follows with the full equation.

---

## PART 4 — OLS (Anims 13–17, 4:30–7:00)

### TEXT-F: Why square errors — 4 reasons  ← INSERT BETWEEN Anim14 and Anim15
**Style:** BulletReveal — 4 bullets appear one by one
**Content (from HTML card):**
  • Raw errors cancel out — positive and negative offset each other
  • Squaring makes all errors positive — they can't cancel
  • Squaring penalises large errors MORE than small ones
  • Squared function is differentiable — needed for calculus optimisation
**Duration:** ~10 seconds
**Why here:** Ball just slid down the bowl (Anim14). Before showing the 
  cancellation animation (Anim15), plant the 4 reasons. Then Anim15 
  visually demonstrates reason #1 (errors cancel).

### TEXT-G: Normal Equation 6-step derivation  ← INSERT BETWEEN Anim16 and Anim17
**Style:** BulletReveal — numbered steps appear one by one (fast, ~1s each)
**Content:**
  1.  Write cost:   J = (1/n)(y − Xβ)ᵀ(y − Xβ)
  2.  Expand:       J = (1/n)(yᵀy − 2βᵀXᵀy + βᵀXᵀXβ)
  3.  Differentiate:  ∂J/∂β = (1/n)(−2Xᵀy + 2XᵀXβ)
  4.  Set to zero:   −2Xᵀy + 2XᵀXβ = 0
  5.  Rearrange:    XᵀXβ = Xᵀy  (the "normal equations")
  6.  Solve:        β = (XᵀX)⁻¹Xᵀy  ✓
**Duration:** ~12 seconds
**Why here:** Global minimum just appeared with its marker (Anim16). 
  The derivation explains HOW that formula was derived analytically. 
  Then Anim17 shows the formula with the warning card.
**Note:** This is the most math-heavy text block. Keep font small (18pt), 
  use monospace for the equations, keep each step on screen for ~1.5s.

---

## PART 5 — GRADIENT DESCENT (Anims 18–20, 7:00–9:00)

### TEXT-H: Gradient descent 6-step algorithm  ← INSERT BETWEEN Anim19 and Anim20
**Style:** BulletReveal — numbered, with the update rule formula prominent at top
**Content:**
  Formula at top: β ← β − α × (−2/n) Xᵀ(y − Xβ)
  Then steps:
  1. Initialise β (zeros or small random values)
  2. Compute predictions: ŷ = Xβ
  3. Compute residuals:  e = y − ŷ
  4. Compute gradient:   ∇ = −(2/n) Xᵀe
  5. Update:             β ← β − α × ∇
  6. Repeat until ‖∇‖ < ε or max iterations reached
**Duration:** ~12 seconds
**Why here:** Anim19 showed the ball stepping down the bowl — the visual.
  Now the algorithm lists the exact steps the computer does. Then Anim20 
  shows what happens to those steps when α is wrong.

### TEXT-I: GD types comparison  ← INSERT AFTER Anim20
**Style:** TableBuild — 3 rows, 3 columns (simplified from HTML's 5-column table)
**Content:**
  | Type       | Batch Size | Best For                    |
  | Batch GD   | All n      | Small datasets, stable      |
  | SGD        | 1          | Huge datasets, online       |
  | Mini-batch | 16–512     | Deep learning, GPU training |
**Duration:** ~8 seconds
**Why here:** Learning rates just covered. Natural extension: "and there 
  are three flavours of how many samples you use per step."

---

## PART 6 — LINE-MO ASSUMPTIONS (Anims 21–28, 9:00–11:30)

### TEXT-J: Misconception callout for N  ← INSERT INSIDE Anim24 (N-Normality)
**Style:** CardFlip (Red/warning border) — appears AFTER the histograms
**Content:** "⚠ COMMON MISCONCEPTION:
  This assumption is about the RESIDUALS — not the raw X data, not y.
  Your input features can be skewed, uniform, or anything.
  With n > 30+, the Central Limit Theorem makes this less critical anyway."
**Duration:** ~8 seconds (replaces the current simple fix text at the bottom)
**Why here:** This is the single most important misconception in the entire 
  HTML (it even has a special callout div). Must be on screen.

### TEXT-K: Detection methods summary  ← INSERT AFTER Anim28 (all letters glow)
**Style:** TableBuild — 6 rows, 2 columns
**Content:**
  | Assumption     | How to Detect                          |
  | L Linearity    | Residuals vs. Fitted plot — U-shape?   |
  | I Independence | Durbin-Watson test (~2 = OK)            |
  | N Normality    | Q-Q plot — points on diagonal?         |
  | E Equal Var.   | Scale-Location plot — flat line?       |
  | M Multicollin. | VIF > 5 = warning, VIF > 10 = severe   |
  | O Outliers     | Cook's Distance > 4/n = investigate    |
**Duration:** ~12 seconds
**Why here:** After all 6 assumptions are shown, this table gives the 
  practical diagnostic toolkit in one place. Viewer can screenshot this.

---

## PART 7 — METRICS (Anims 29–31, 11:30–13:30)

### TEXT-L: R² interpretation table  ← INSERT BETWEEN Anim30 and Anim31
**Style:** TableBuild — 6 rows, colour-coded
**Content (from HTML):**
  | R² Value | Interpretation              | Context                    |
  | < 0      | Worse than predicting mean  | Model broken or leakage    |
  | 0.0      | No better than baseline     | Features explain nothing   |
  | 0.3–0.5  | Moderate                    | Social science, economics  |
  | 0.7–0.9  | Good                        | Typical ML regression      |
  | 0.95+    | Excellent                   | Engineering, physics       |
  | 1.0      | Suspicious — check leakage  | Likely data leak           |
**Duration:** ~10 seconds
**Why here:** R² warning just flashed (Anim30). Before showing the 
  counter (Anim31), give viewers the benchmark table. The 1.0 = suspicious 
  row is a particularly memorable insight.

### TEXT-M: MAE vs RMSE decision rule  ← INSERT AFTER Anim31
**Style:** SplitReveal — left panel MAE, right panel RMSE
**Content:**
  Left (Blue): USE MAE WHEN
  • Outliers exist and shouldn't dominate
  • Business cares equally about all error sizes
  • Explaining to non-technical stakeholders
  Right (Orange): USE RMSE WHEN
  • Large errors are disproportionately costly
  • Engineering, finance, structural prediction
  • Competing in Kaggle (RMSE is standard)
**Duration:** ~10 seconds
**Why here:** Viewer just watched R² vs Adj R² counter (Anim31). Natural 
  next question: "ok so which metric do I actually use day to day?"

---

## PART 8 — REGULARIZATION (Anims 32–36, 13:30–16:00)

### TEXT-N: Ridge key facts  ← INSERT BETWEEN Anim33 and Anim34
**Style:** BulletReveal — 4 bullets (kept short, 1 line each)
**Content:**
  • Closed-form: β = (XᵀX + λI)⁻¹Xᵀy — always invertible
  • λ = 0 → plain OLS   |   λ → ∞ → all β → 0
  • Distributes weight across correlated features (doesn't pick one)
  • Never produces exact zeros — keeps all features in the model
**Duration:** ~8 seconds
**Why here:** Penalty term just appeared (Anim33). These 4 bullets are 
  the "what Ridge actually does" before the geometry (Anim34) shows WHY.

### TEXT-O: Lasso key facts  ← INSERT BETWEEN Anim34 and Anim35
**Style:** BulletReveal — 4 bullets
**Content:**
  • No closed form — uses iterative coordinate descent
  • With correlated features: arbitrarily picks one, zeros the others
  • Produces sparse models — great for thousands of features (genomics, text)
  • Too high λ → important features get zeroed out too
**Duration:** ~8 seconds
**Why here:** Ridge geometry just shown (Anim34). Before Lasso geometry 
  (Anim35), give the contrast: "here's what Lasso does differently."

### TEXT-P: L1 sparsity — calculus answer  ← INSERT BETWEEN Anim35 and Anim36
**Style:** SplitReveal — left Geometric, right Calculus
**Content (from HTML interview box — this is genuinely teachable):**
  Left (Blue): GEOMETRIC
  "Diamond corners sit on axes.
  MSE ellipse almost always first
  touches a corner → β = exactly 0"
  Right (Orange): CALCULUS  
  "L2 derivative = 2βⱼ → shrinks
  proportionally → approaches 0,
  never reaches it.
  L1 derivative = sign(βⱼ) → constant
  push toward 0 → can reach exactly 0"
**Duration:** ~10 seconds
**Why here:** This is the single most asked interview question about 
  regularisation. It directly supplements the geometry (Anim35) with 
  the algebraic explanation. Both are in the HTML.

---

## PART 9 — BIAS-VARIANCE (Anims 37–38, 16:00–17:30)

### TEXT-Q: Error decomposition table  ← INSERT BETWEEN Anim37 and Anim38
**Style:** TableBuild — 3 rows
**Content:**
  | Component          | Caused by                  | Fixed by                    |
  | Bias²              | Too simple, wrong model    | More features, polynomial   |
  | Variance           | Too complex, overfitting   | Regularisation, more data   |
  | Irreducible Noise  | True randomness in data    | Cannot be reduced — floor   |
**Duration:** ~8 seconds
**Why here:** Three curves just animated in (Anim37). Before the sweet 
  spot pulses (Anim38), explain what each curve actually represents 
  in practical terms.

### TEXT-R: Regularisation-bias-variance connection  ← INSERT AFTER Anim38
**Style:** BulletReveal — 4 bullets
**Content (from HTML table):**
  • OLS with few features, non-linear data → High Bias → add polynomial features
  • OLS with many features, p ≈ n → High Variance → use Ridge or Lasso
  • Ridge with high λ → Moderate Bias, Low Variance → reduce λ
  • Ridge with λ ≈ 0 → Very Low Bias, High Variance → increase λ
**Duration:** ~10 seconds
**Why here:** Sweet spot just pulsed. This maps the abstract tradeoff to 
  concrete model choices viewers can actually make.

---

## PART 10 — CV & PIPELINE (Anims 39–42, 17:30–19:00)

### TEXT-S: Data leakage forms  ← INSERT BETWEEN Anim40 and Anim41
**Style:** BulletReveal — 4 bullets (red text, warning style)
**Content (from HTML interview Q11):**
  Other leakage forms beyond scaling:
  • Target encoding computed on full data before split
  • Feature selection using all data before splitting
  • Missing value imputation using the full dataset's mean
  • Hyperparameters tuned using test set performance
**Duration:** ~8 seconds
**Why here:** Wrong approach just shown (Anim40). Before the correct 
  pipeline (Anim41), expand "leakage is bigger than just scaling."

### TEXT-T: Pipeline benefits  ← INSERT BETWEEN Anim41 and Anim42
**Style:** BulletReveal — 4 bullets (green, positive framing)
**Content:**
  • Fit once: pipeline.fit(X_train) — scaler sees only train data
  • Predict safely: pipeline.predict(X_test) — uses train statistics
  • CV-compatible: works seamlessly with GridSearchCV / cross_val_score
  • Serialisable: joblib.dump(pipeline) saves scaler + model together
**Duration:** ~8 seconds
**Why here:** Bridges the "why correct" (Anim41) with the "how it looks 
  in code" (Anim42 pipeline diagram).

---

## OUTRO (Anim 43–44, 19:00–19:45)

### TEXT-U: Production workflow  ← INSERT BETWEEN Anim43 and Anim44
**Style:** BulletReveal — numbered, fast (0.8s per step)
**Content (HTML Q12 answer condensed):**
  The 9-step production workflow:
  1. EDA — distributions, correlations, missing values
  2. Preprocessing — impute, encode, log-transform, scale → Pipeline
  3. Baseline — plain OLS, get train + 5-fold CV metrics
  4. Diagnostics — 4 plots: Residuals, Q-Q, Scale-Location, Cook's D
  5. Fix violations — transform, remove collinear features
  6. Regularise — try RidgeCV, LassoCV, ElasticNet
  7. Interpret — standardised coefficients, CIs via statsmodels
  8. Final evaluation — test set ONCE, report RMSE / MAE / R²
  9. Deploy — joblib.dump(pipeline), monitor for data drift
**Duration:** ~14 seconds
**Why here:** Summary screen (Anim43) shows the concepts. This list 
  tells viewers HOW to apply them in order. It's the practical takeaway 
  that differentiates this video from a textbook explanation.

---

## WHAT TO SKIP ENTIRELY (not animated, not spoken)

These sections from the HTML are valuable as reference material but wrong 
for video — too detailed, too tabular, or too code-heavy:

**Skip:** Full 8-item pros/cons list for overall Linear Regression.
  (Mentioned verbally in parts, not worth 2 minutes of bullets)

**Skip:** All hyperparameter tables (fit_intercept, copy_X, solver, tol, 
  max_iter, warm_start etc.) — this is reference documentation. 
  Link to the HTML in the description.

**Skip:** Feature Engineering section entirely (Sections 9: transformations,
  interactions, encoding, scaling tables) — this is a separate video topic.
  Can mention: "feature engineering for linear regression — next video."

**Skip:** Full Python sklearn code (Sections 12) — link in description.

**Skip:** Interview Q&As 1–10 as separate Q&A segments — too long, breaks 
  video pacing. The key insight from each relevant Q&A is already folded into 
  TEXT-C, TEXT-E, TEXT-J, TEXT-P, TEXT-R above.

**Skip:** ElasticNet deep dive — worth a mention in the Ridge/Lasso section 
  verbally ("ElasticNet combines both — for another video").

**Skip:** Residual diagnostics section (Section 8) as standalone — Cook's 
  distance etc. is a separate video topic. The LINE-MO animations already 
  cover what matters for understanding.

---

## SUMMARY: 21 TEXT ANIMATIONS, EXACT INSERTION POINTS

| ID     | Content                         | Style         | Goes Between        | Duration |
|--------|---------------------------------|---------------|---------------------|----------|
| TEXT-A | What/How/Why cards              | CardFlip      | Anim02 → Anim03     | 8s       |
| TEXT-B | Simple vs Multiple table        | TableBuild    | Anim03 → Anim04     | 6s       |
| TEXT-C | Residual definition box         | CardFlip      | Anim06 → Anim07     | 7s       |
| TEXT-D | Symbol table (ŷ β x)           | TableBuild    | Anim10 → Anim11     | 10s      |
| TEXT-E | Coefficient scaling warning     | CardFlip      | Anim11 → Anim12     | 8s       |
| TEXT-F | Why square errors (4 reasons)   | BulletReveal  | Anim14 → Anim15     | 10s      |
| TEXT-G | Normal Eq 6-step derivation     | BulletReveal  | Anim16 → Anim17     | 12s      |
| TEXT-H | GD 6-step algorithm             | BulletReveal  | Anim19 → Anim20     | 12s      |
| TEXT-I | GD types table                  | TableBuild    | Anim20 → Anim21     | 8s       |
| TEXT-J | Normality misconception card    | CardFlip      | inside Anim24       | 8s       |
| TEXT-K | Detection methods table         | TableBuild    | Anim28 → Anim29     | 12s      |
| TEXT-L | R² interpretation table         | TableBuild    | Anim30 → Anim31     | 10s      |
| TEXT-M | MAE vs RMSE decision            | SplitReveal   | Anim31 → Anim32     | 10s      |
| TEXT-N | Ridge key facts                 | BulletReveal  | Anim33 → Anim34     | 8s       |
| TEXT-O | Lasso key facts                 | BulletReveal  | Anim34 → Anim35     | 8s       |
| TEXT-P | L1 sparsity explanation         | SplitReveal   | Anim35 → Anim36     | 10s      |
| TEXT-Q | Error decomposition table       | TableBuild    | Anim37 → Anim38     | 8s       |
| TEXT-R | Regularisation-BV connection    | BulletReveal  | Anim38 → Anim39     | 10s      |
| TEXT-S | Leakage forms                   | BulletReveal  | Anim40 → Anim41     | 8s       |
| TEXT-T | Pipeline benefits               | BulletReveal  | Anim41 → Anim42     | 8s       |
| TEXT-U | 9-step production workflow      | BulletReveal  | Anim43 → Anim44     | 14s      |

Total text animation time added: ~3 minutes 5 seconds
New estimated video length: ~21–23 minutes

---

## HOW TO IMPLEMENT THESE IN MANIM

Each style is a reusable scene class. Here is the pattern for each:

### CardFlip pattern:
```python
class TextA_WhatHowWhy(Scene):
    def construct(self):
        self.camera.background_color = "#0d0f14"
        cards = [
            ("WHAT", "#4f9eff", "Finds best-fit line..."),
            ("HOW",  "#10b981", "Minimises squared..."),
            ("WHY",  "#f97316", "Interpretable, fast..."),
        ]
        for title, color, body in cards:
            bg = RoundedRectangle(corner_radius=0.15, width=10, height=1.6,
                fill_color="#13161e", fill_opacity=1,
                stroke_color=color, stroke_width=2)
            t = Text(title, font_size=22, color=color, weight=BOLD)\
                .next_to(bg.get_left(), RIGHT, buff=0.3)
            b = Text(body, font_size=19, color="#c8d0dc")\
                .next_to(t, RIGHT, buff=0.4)
            grp = VGroup(bg, t, b).shift(...)  # position per card
            self.play(FadeIn(bg), Write(t), FadeIn(b), run_time=0.7)
            self.wait(1.5)
            self.play(FadeOut(grp), run_time=0.4)
```

### BulletReveal pattern:
```python
class TextF_WhySquareErrors(Scene):
    def construct(self):
        self.camera.background_color = "#0d0f14"
        title = Text("Why Square the Errors?", font_size=26, color="#f8fafc")\
            .to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)
        bullets = [
            "Raw errors cancel — positive and negative offset each other",
            "Squaring makes all errors positive — they can't cancel",
            "Squaring penalises LARGE errors far more than small ones",
            "Squared function is differentiable — required for calculus",
        ]
        bullet_group = VGroup()
        for i, text in enumerate(bullets):
            dot = Text("•", font_size=22, color="#4f9eff")
            line = Text(text, font_size=20, color="#c8d0dc")
            row = VGroup(dot, line).arrange(RIGHT, buff=0.2)
            row.move_to(UP * (0.8 - i * 0.85))
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(1.2)
```

### TableBuild pattern:
```python
class TextK_DetectionMethods(Scene):
    def construct(self):
        headers = ["Assumption", "How to Detect"]
        rows = [
            ["L  Linearity",    "Residuals vs. Fitted — U-shape?"],
            ["I  Independence", "Durbin-Watson test (~2 = OK)"],
            ...
        ]
        # Build header row first, then animate data rows one at a time
        # Each row: FadeIn(row, shift=RIGHT * 0.2), wait(0.8)
```

### SplitReveal pattern:
```python
class TextM_MAEvsRMSE(Scene):
    def construct(self):
        divider = Line(UP*3.5, DOWN*3.5, color="#252a38", stroke_width=1.5)
        left_title  = Text("USE MAE WHEN", color="#4f9eff", ...)
        right_title = Text("USE RMSE WHEN", color="#f97316", ...)
        self.play(Create(divider), Write(left_title), Write(right_title))
        # Then bullets appear on each side alternately
```

---

## IMPORTANT NOTES FOR PRODUCTION

1. **These 21 text scenes are SHORT** — 6–14 seconds each. Don't let them 
   drag. If a bullet point is on screen, your voiceover should be reading it.
   No silent text.

2. **Font consistency:** Use the same font family throughout. Lato or Inter 
   for body text. For math/code use Courier New or Source Code Pro.
   Manim's default font works fine — just be consistent.

3. **Don't crowd the screen.** Max 4 bullets visible at once. If a table 
   has more than 6 rows, split it across two scenes or trim it.

4. **The existing 44 Anim scenes are NOT affected.** These 21 text scenes 
   slot between them. Your rendering workflow stays the same — render each 
   file, then assemble in DaVinci Resolve in the order shown in the summary table.

5. **TEXT-J is the only one that modifies an existing scene** (Anim24). 
   The CardFlip content replaces the current simple "fix" line. Just edit the 
   `fix` text variable in Anim24_N_Normality to the fuller misconception callout.
