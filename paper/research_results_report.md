# XAI-CDSS Research Results

Generated from saved experimental outputs only. No models were retrained and no SHAP, LIME, or counterfactual search was rerun during report generation.

## Held-out Model Performance

| disease                |   accuracy |   precision |   recall_sensitivity |   specificity |       f1 |   roc_auc |   samples |   tn |   fp |   fn |   tp |
|:-----------------------|-----------:|------------:|---------------------:|--------------:|---------:|----------:|----------:|-----:|-----:|-----:|-----:|
| Heart Disease          |   0.885246 |    0.818182 |             0.964286 |      0.818182 | 0.885246 |  0.951299 |        61 |   27 |    6 |    1 |   27 |
| Diabetes               |   0.884615 |    0.861111 |             0.96875  |      0.75     | 0.911765 |  0.859375 |       104 |   30 |   10 |    2 |   62 |
| Chronic Kidney Disease |   0.625    |    0.625    |             1        |      0        | 0.769231 |  0.976667 |        80 |    0 |   30 |    0 |   50 |
| Stroke                 |   0.927593 |    0.306452 |             0.38     |      0.955761 | 0.339286 |  0.843827 |      1022 |  929 |   43 |   31 |   19 |

## SHAP–LIME Agreement

| disease   |   patients_evaluated |   agreement_valid_cases |   mean_feature_agreement_pct |   mean_direction_agreement_pct |   mean_ranking_agreement_pct |   mean_overall_consistency_pct |
|:----------|---------------------:|------------------------:|-----------------------------:|-------------------------------:|-----------------------------:|-------------------------------:|
| heart     |                   25 |                      25 |                         59.2 |                            100 |                      63.5828 |                        72.7552 |
| diabetes  |                   25 |                      25 |                         20   |                            100 |                     100      |                        68      |
| ckd       |                   25 |                      25 |                         60.8 |                            100 |                      74.084  |                        76.5448 |
| stroke    |                   25 |                      25 |                         46.4 |                            100 |                      82.5004 |                        73.31   |

## Counterfactual Evaluation

| disease   |   patients_evaluated |   counterfactual_valid_cases |   counterfactual_success_cases |   counterfactual_success_rate_pct |   mean_cf_count |   mean_cf_feature_count |   mean_shap_cf_alignment_pct |   mean_lime_cf_alignment_pct |   mean_common_cf_alignment_pct |
|:----------|---------------------:|-----------------------------:|-------------------------------:|----------------------------------:|----------------:|------------------------:|-----------------------------:|-----------------------------:|-------------------------------:|
| heart     |                   25 |                           25 |                             22 |                                88 |            4.12 |                    3.68 |                      68.6364 |                      27.1591 |                        21.4773 |
| diabetes  |                   25 |                           25 |                             25 |                               100 |            5    |                    4    |                      75      |                       0      |                         0      |
| ckd       |                   25 |                           25 |                              0 |                                 0 |            0    |                    0    |                     nan      |                     nan      |                       nan      |
| stroke    |                   25 |                           25 |                              0 |                                 0 |            0    |                    0    |                     nan      |                     nan      |                       nan      |

## Explanation Stability Statistics

| disease   | metric        |   n |     mean |       std |   median |   iqr |
|:----------|:--------------|----:|---------:|----------:|---------:|------:|
| heart     | SHAP Spearman |  50 | 0.875649 | 0.271836  |      1   | 0.175 |
| heart     | LIME Spearman |  50 | 0.906312 | 0.149755  |      1   | 0.1   |
| diabetes  | SHAP Spearman |  50 | 0.844    | 0.317619  |      1   | 0.2   |
| diabetes  | LIME Spearman |  50 | 0.928    | 0.142914  |      1   | 0.1   |
| ckd       | SHAP Spearman |  50 | 1        | 0         |      1   | 0     |
| ckd       | LIME Spearman |  50 | 0.853715 | 0.208217  |      0.9 | 0.2   |
| stroke    | SHAP Spearman |  50 | 0.998    | 0.0141421 |      1   | 0     |
| stroke    | LIME Spearman |  50 | 0.998    | 0.0141421 |      1   | 0     |

## Interpretation Notes

- The held-out model metrics describe the saved production classifiers evaluated on the saved real test sets.
- SHAP–LIME agreement measures consistency between post-hoc explanation methods; agreement does not establish causal correctness.
- Counterfactuals are model-validated what-if scenarios, not clinical treatment recommendations.
- For diseases with zero successful counterfactual cases, SHAP/LIME counterfactual-alignment statistics are reported as N/A rather than zero because no successful counterfactual set exists for comparison.
- The perturbation experiment is a controlled local stability stress test, not external clinical robustness or clinical validation.
- Post-hoc explanation components do not retrain the classifier; therefore their addition should not be described as improving classification accuracy.
- The saved Heart augmentation experiment is reported separately and should not be generalized as an all-disease augmentation comparison.

## Available Baseline Evidence

| disease       | metric    |   real_only |   real_plus_synthetic |   improvement | evidence_type             |
|:--------------|:----------|------------:|----------------------:|--------------:|:--------------------------|
| Heart Disease | Accuracy  |    0.885246 |              0.852459 |    -0.0327869 | Existing saved experiment |
| Heart Disease | Precision |    0.818182 |              0.88     |     0.0618182 | Existing saved experiment |
| Heart Disease | Recall    |    0.964286 |              0.785714 |    -0.178571  | Existing saved experiment |
| Heart Disease | F1 Score  |    0.885246 |              0.830189 |    -0.0550572 | Existing saved experiment |
| Heart Disease | ROC-AUC   |    0.955087 |              0.923701 |    -0.0313853 | Existing saved experiment |

## Post-hoc Component Analysis

| disease   |   accuracy |   precision |   recall |       f1 |   roc_auc | configuration            |   explanation_coverage_pct |   feature_agreement_pct |   overall_consistency_pct |   counterfactual_success_rate_pct | note                                                                                             |
|:----------|-----------:|------------:|---------:|---------:|----------:|:-------------------------|---------------------------:|------------------------:|--------------------------:|----------------------------------:|:-------------------------------------------------------------------------------------------------|
| heart     |   0.885246 |    0.818182 | 0.964286 | 0.885246 |  0.951299 | Prediction only          |                        nan |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| heart     |   0.885246 |    0.818182 | 0.964286 | 0.885246 |  0.951299 | Prediction + SHAP        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| heart     |   0.885246 |    0.818182 | 0.964286 | 0.885246 |  0.951299 | Prediction + LIME        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| heart     |   0.885246 |    0.818182 | 0.964286 | 0.885246 |  0.951299 | Prediction + SHAP + LIME |                        nan |                    59.2 |                   72.7552 |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| heart     |   0.885246 |    0.818182 | 0.964286 | 0.885246 |  0.951299 | Full XAI-CDSS            |                        nan |                    59.2 |                   72.7552 |                                88 | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| diabetes  |   0.884615 |    0.861111 | 0.96875  | 0.911765 |  0.859375 | Prediction only          |                        nan |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| diabetes  |   0.884615 |    0.861111 | 0.96875  | 0.911765 |  0.859375 | Prediction + SHAP        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| diabetes  |   0.884615 |    0.861111 | 0.96875  | 0.911765 |  0.859375 | Prediction + LIME        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| diabetes  |   0.884615 |    0.861111 | 0.96875  | 0.911765 |  0.859375 | Prediction + SHAP + LIME |                        nan |                    20   |                   68      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| diabetes  |   0.884615 |    0.861111 | 0.96875  | 0.911765 |  0.859375 | Full XAI-CDSS            |                        nan |                    20   |                   68      |                               100 | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| ckd       |   0.625    |    0.625    | 1        | 0.769231 |  0.976667 | Prediction only          |                        nan |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| ckd       |   0.625    |    0.625    | 1        | 0.769231 |  0.976667 | Prediction + SHAP        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| ckd       |   0.625    |    0.625    | 1        | 0.769231 |  0.976667 | Prediction + LIME        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| ckd       |   0.625    |    0.625    | 1        | 0.769231 |  0.976667 | Prediction + SHAP + LIME |                        nan |                    60.8 |                   76.5448 |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| ckd       |   0.625    |    0.625    | 1        | 0.769231 |  0.976667 | Full XAI-CDSS            |                        nan |                    60.8 |                   76.5448 |                                 0 | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| stroke    |   0.927593 |    0.306452 | 0.38     | 0.339286 |  0.843827 | Prediction only          |                        nan |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| stroke    |   0.927593 |    0.306452 | 0.38     | 0.339286 |  0.843827 | Prediction + SHAP        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| stroke    |   0.927593 |    0.306452 | 0.38     | 0.339286 |  0.843827 | Prediction + LIME        |                        100 |                   nan   |                  nan      |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| stroke    |   0.927593 |    0.306452 | 0.38     | 0.339286 |  0.843827 | Prediction + SHAP + LIME |                        nan |                    46.4 |                   73.31   |                               nan | Post-hoc component analysis. Classification metrics are from the same held-out production model. |
| stroke    |   0.927593 |    0.306452 | 0.38     | 0.339286 |  0.843827 | Full XAI-CDSS            |                        nan |                    46.4 |                   73.31   |                                 0 | Post-hoc component analysis. Classification metrics are from the same held-out production model. |

## Heart Augmentation Experiment

|   synthetic rows |   total training rows |   accuracy |   precision |   recall |   f1 score |   roc-auc |   accuracy change |   precision change |   recall change |   f1 change |   roc-auc change |
|-----------------:|----------------------:|-----------:|------------:|---------:|-----------:|----------:|------------------:|-------------------:|----------------:|------------:|-----------------:|
|                0 |                   242 |   0.885246 |    0.818182 | 0.964286 |   0.885246 |  0.955087 |         0         |          0         |       0         |  0          |        0         |
|              500 |                   742 |   0.868852 |    0.794118 | 0.964286 |   0.870968 |  0.927489 |        -0.0163934 |         -0.0240642 |       0         | -0.0142782  |       -0.0275974 |
|             1000 |                  1242 |   0.819672 |    0.774194 | 0.857143 |   0.813559 |  0.922078 |        -0.0655738 |         -0.0439883 |      -0.107143  | -0.0716866  |       -0.0330087 |
|             2000 |                  2242 |   0.852459 |    0.851852 | 0.821429 |   0.836364 |  0.944805 |        -0.0327869 |          0.03367   |      -0.142857  | -0.0488823  |       -0.0102814 |
|             5000 |                  5242 |   0.901639 |    0.892857 | 0.892857 |   0.892857 |  0.928571 |         0.0163934 |          0.0746753 |      -0.0714286 |  0.00761124 |       -0.0265152 |

## Research Contribution Wording

> We propose a unified explanation-reliability framework for tabular clinical decision support that jointly evaluates model predictions, local feature attributions from SHAP and LIME, cross-explainer agreement, explanation stability under controlled perturbations, and model-validated counterfactual decision-boundary behavior. The framework further measures the alignment between influential explanation features and features involved in successful counterfactual transitions.

## Limitations

- Counterfactuals are model-based what-if scenarios and are not clinical treatment recommendations.
- The current perturbation experiment is a local robustness/stability stress test, not external clinical validation.
- Agreement indicates consistency between explanation methods; it does not by itself establish causal correctness.
- The stability study used 10 real test patients per disease and 5 perturbations per patient; it is a pilot-scale evaluation rather than a large external validation study.
- The saved augmentation comparison is currently available for Heart Disease only.
- Any novelty statement should use cautious wording such as 'we propose' or 'we introduce' unless established by a systematic literature review.
