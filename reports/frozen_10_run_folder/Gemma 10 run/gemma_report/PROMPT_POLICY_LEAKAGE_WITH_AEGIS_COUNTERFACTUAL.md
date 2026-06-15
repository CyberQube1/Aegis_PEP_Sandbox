# Prompt-Policy Leakage With Aegis Counterfactual

This report lists prompt-policy rows where the prompt-policy condition allowed and applied a mock tool while the scoring flags marked the row as a policy-risk completion. It then joins the Aegis-governed row for the same run/task where available.

Interpretation notes:
- These rows are prompt-policy leakage rows, not Aegis-governed side effects.
- Aegis counterfactual fields show what the governed Aegis/PDP path did for the same run/task.
- A settled Senate allow does not mean the original mock tool was applied unless the governed row has `aegis_counterfactual_mock_tool_applied=true`.
- `policy_risk_effect_summary` is an operational/policy impact label derived from task category and scoring flags; it is not a dollar-cost estimate.

No prompt-policy leakage rows found in selected runs.
