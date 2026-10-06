# Contributing

Change a decision rule only for a demonstrated failure or a missing concrete
requirement. Keep shared rules in the entry point and conditional guidance in
focused references. Avoid repeating standard knowledge and accumulating rules
from a single anecdote.

Run the checks in [README.md](README.md). For a change to instructions, include a
realistic behavioral prompt and inspect the consuming agent's actions/artifacts.
Tests that merely search prose for the desired words do not show instruction
compliance. For the evidence gate, add a regression that exercises its real
inputs and failure behavior.

Use [the evaluation protocol](evals/README.md) for comparative claims. Report
failures and limits as well as successes; keep raw traces and measurements private.
Never include real credentials, user data, machine paths, or proprietary code.
Submit small coherent diffs and preserve upstream attribution when incorporating
material under a compatible license.
