################################################################################
# run_parallel_windows.ps1
# Renders all 66 scenes in parallel using PowerShell background jobs.
# Run from PowerShell (NOT cmd.exe).
#
# USAGE:
#   .\run_parallel_windows.ps1                  # low quality, 4 workers
#   .\run_parallel_windows.ps1 -Quality ql      # low   (default, fastest)
#   .\run_parallel_windows.ps1 -Quality qm      # medium
#   .\run_parallel_windows.ps1 -Quality qh      # high
#   .\run_parallel_windows.ps1 -Workers 6       # 6 parallel jobs
#   .\run_parallel_windows.ps1 -Quality qm -Workers 8
#
# NOTES:
#   - Each worker runs one manim command at a time.
#   - Workers=4 is safe for most systems (4 CPU cores).
#   - Workers=CPU_count is max parallelism but may cause RAM issues.
#   - Logs for each scene are saved to logs\SceneXX.log
#   - If execution policy blocks this script, run:
#       Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
################################################################################

param(
    [string]$Quality = "ql",
    [int]$Workers = 4
)

$File     = "per_scene_classes.py"
$LogDir   = "logs"

$Scenes = @(
    "Scene01Intro",
    "Scene02WhatIs",
    "Scene03FiveWs",
    "Scene04WhyLinearFails",
    "Scene05OverallProsCons",
    "Scene06HillyRoad",
    "Scene07FeatureEngineering",
    "Scene08RealWorld",
    "Scene09Equation",
    "Scene10DegreeShapes",
    "Scene11WhyLinear",
    "Scene12NormalEquations",
    "Scene13NormalEqProsCons",
    "Scene14CostGd",
    "Scene15GdProsCons",
    "Scene16AssumptionsLinemo",
    "Scene17AssumptionLinearity",
    "Scene18AssumptionIndependence",
    "Scene19AssumptionNormality",
    "Scene20AssumptionHomoscedasticity",
    "Scene21AssumptionMulticollinearity",
    "Scene22MulticollinearityProsCons",
    "Scene23AssumptionOutliers",
    "Scene24BiasVariance",
    "Scene25BvChart",
    "Scene26FittingCards",
    "Scene27Overfitting",
    "Scene28Runge",
    "Scene29OverfittingProsCons",
    "Scene30Underfitting",
    "Scene31VisualInspection",
    "Scene32CrossValidation",
    "Scene33LearningCurves",
    "Scene34AicBic",
    "Scene35AdjustedR2",
    "Scene36ErrorCurve",
    "Scene37RegularisationOverview",
    "Scene38Ridge",
    "Scene39Lasso",
    "Scene40Elasticnet",
    "Scene41RegComparison",
    "Scene42AlphaEffect",
    "Scene43FeatureScaling",
    "Scene44StandardScaler",
    "Scene45Minmax",
    "Scene46Centering",
    "Scene47FeatureExplosion",
    "Scene48ExplosionProsCons",
    "Scene49MseRmse",
    "Scene50MaeR2",
    "Scene51AdjR2Mape",
    "Scene52CiPi",
    "Scene53Pipeline",
    "Scene54HpPoly",
    "Scene55HpRidge",
    "Scene56HpLassoEnet",
    "Scene57OverallProsCons",
    "Scene58WhenToUse",
    "Scene59Alternatives",
    "Scene60Mistakes",
    "Scene61IqLinear",
    "Scene62IqOverfit",
    "Scene63IqTrainTest",
    "Scene64IqScale",
    "Scene65IqLassoZeros",
    "Scene66Outro"
)

# Create log directory
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

$Total     = $Scenes.Count
$Queue     = [System.Collections.Queue]::new($Scenes)
$Running   = @{}
$Done      = 0
$Failed    = @()
$StartTime = Get-Date

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Polynomial Regression - Parallel Render" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Scenes  : $Total"
Write-Host " Workers : $Workers"
Write-Host " Quality : -$Quality"
Write-Host " File    : $File"
Write-Host " Logs    : .\$LogDir\"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Main loop
while ($Queue.Count -gt 0 -or $Running.Count -gt 0) {

    # Start new jobs up to worker limit
    while ($Queue.Count -gt 0 -and $Running.Count -lt $Workers) {
        $Scene   = $Queue.Dequeue()
        $LogFile = Join-Path $LogDir "$Scene.log"
        $Job     = Start-Job -ScriptBlock {
            param($q, $f, $s, $log)
            $cmd = "manim -$q $f $s"
            $output = & manim "-$q" $f $s 2>&1
            $output | Out-File $log -Encoding utf8
            if ($LASTEXITCODE -ne 0) { exit 1 }
        } -ArgumentList $Quality, $File, $Scene, $LogFile
        $Running[$Scene] = $Job
        Write-Host "  START  $Scene" -ForegroundColor Yellow
    }

    # Check for finished jobs
    $Finished = @()
    foreach ($entry in $Running.GetEnumerator()) {
        $Scene = $entry.Key
        $Job   = $entry.Value
        if ($Job.State -in @("Completed", "Failed", "Stopped")) {
            $Done++
            $ExitCode = Receive-Job -Job $Job -ErrorAction SilentlyContinue
            Remove-Job -Job $Job
            if ($Job.State -eq "Completed") {
                Write-Host "  DONE   [$Done/$Total] $Scene" -ForegroundColor Green
            } else {
                Write-Host "  FAIL   [$Done/$Total] $Scene  (see $LogDir\$Scene.log)" -ForegroundColor Red
                $Failed += $Scene
            }
            $Finished += $Scene
        }
    }
    foreach ($s in $Finished) { $Running.Remove($s) }

    if ($Running.Count -gt 0 -or $Queue.Count -gt 0) {
        Start-Sleep -Milliseconds 500
    }
}

$Elapsed = (Get-Date) - $StartTime
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " RENDER COMPLETE" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Total   : $Total scenes"
Write-Host " Elapsed : $($Elapsed.ToString('mm\:ss'))"
Write-Host " Output  : media\videos\per_scene_classes\"
if ($Failed.Count -gt 0) {
    Write-Host " FAILED  : $($Failed.Count) scenes" -ForegroundColor Red
    foreach ($s in $Failed) {
        Write-Host "   - $s  (log: $LogDir\$s.log)" -ForegroundColor Red
    }
} else {
    Write-Host " Status  : All scenes OK" -ForegroundColor Green
}
Write-Host "============================================" -ForegroundColor Cyan
