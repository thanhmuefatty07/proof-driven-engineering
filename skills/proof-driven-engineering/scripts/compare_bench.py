import argparse
import json
import math
import random
import statistics
import sys
from pathlib import Path

VALID_DIRECTIONS = ("lower_is_better", "higher_is_better")
DEFAULT_BOOTSTRAP_ITERS = 2000
DEFAULT_SEED = 0x5EEDBEEF


def is_real_number(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(float(value))


def quantile(sorted_values: list[float], p: float) -> float:
    n = len(sorted_values)
    if n == 1:
        return sorted_values[0]
    pos = (n - 1) * p
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_values[lo]
    frac = pos - lo
    return sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac


def summarize(samples: list[float]) -> dict[str, float | int]:
    ordered = sorted(samples)
    med = quantile(ordered, 0.50)
    q1 = quantile(ordered, 0.25)
    q3 = quantile(ordered, 0.75)
    abs_devs = sorted(abs(x - med) for x in ordered)
    mad = quantile(abs_devs, 0.50)
    return {
        "n": len(ordered),
        "min": ordered[0],
        "median": med,
        "mean": statistics.fmean(ordered),
        "iqr": q3 - q1,
        "mad": mad,
        "p95": quantile(ordered, 0.95),
        "p99": quantile(ordered, 0.99),
        "max": ordered[-1],
    }


def cliffs_delta(baseline: list[float], candidate: list[float], direction: str) -> float:
    wins = 0
    losses = 0
    for b in baseline:
        for c in candidate:
            if direction == "lower_is_better":
                if b > c:
                    wins += 1
                elif b < c:
                    losses += 1
            else:
                if c > b:
                    wins += 1
                elif c < b:
                    losses += 1
    return (wins - losses) / (len(baseline) * len(candidate))


def mann_whitney_u(baseline: list[float], candidate: list[float]) -> tuple[float, float]:
    n1 = len(baseline)
    n2 = len(candidate)
    combined = [(val, 0) for val in baseline] + [(val, 1) for val in candidate]
    combined.sort(key=lambda item: item[0])
    total = n1 + n2
    rank_sum_1 = 0.0
    tie_correction = 0.0
    i = 0
    while i < total:
        j = i + 1
        while j < total and combined[j][0] == combined[i][0]:
            j += 1
        count = j - i
        avg_rank = 0.5 * ((i + 1) + j)
        for k in range(i, j):
            if combined[k][1] == 0:
                rank_sum_1 += avg_rank
        if count > 1:
            tie_correction += (count ** 3 - count)
        i = j
    u1 = rank_sum_1 - (n1 * (n1 + 1)) / 2.0
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    mean_u = (n1 * n2) / 2.0
    if total <= 1:
        return u, 1.0
    var_u = (n1 * n2 / 12.0) * ((total + 1) - tie_correction / (total * (total - 1)))
    if var_u <= 0.0:
        return u, 1.0
    z = abs(u - mean_u) / math.sqrt(var_u)
    p_value = math.erfc(z / math.sqrt(2.0))
    return u, p_value


def bootstrap_ratio_ci(
    baseline: list[float],
    candidate: list[float],
    direction: str,
    paired: bool,
    iterations: int,
    seed: int = DEFAULT_SEED,
) -> tuple[float, float]:
    rng = random.Random(seed)
    ratios: list[float] = []
    if paired:
        n = len(baseline)
        if direction == "lower_is_better":
            pair_ratios = [b / c for b, c in zip(baseline, candidate)]
        else:
            pair_ratios = [c / b for b, c in zip(baseline, candidate)]
        for _ in range(iterations):
            draw = sorted(pair_ratios[rng.randrange(n)] for _ in range(n))
            ratios.append(quantile(draw, 0.50))
    else:
        n1 = len(baseline)
        n2 = len(candidate)
        for _ in range(iterations):
            b_draw = sorted(baseline[rng.randrange(n1)] for _ in range(n1))
            c_draw = sorted(candidate[rng.randrange(n2)] for _ in range(n2))
            b_med = quantile(b_draw, 0.50)
            c_med = quantile(c_draw, 0.50)
            ratios.append(b_med / c_med if direction == "lower_is_better" else c_med / b_med)
    ratios.sort()
    return quantile(ratios, 0.025), quantile(ratios, 0.975)


def validate_record(record: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["Benchmark record must be a JSON object"]
    if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        errors.append("schema_version must be integer 1")
    for field in ("metric", "unit"):
        val = record.get(field)
        if not isinstance(val, str) or not val.strip():
            errors.append(f"{field} must be a nonempty string")
    direction = record.get("direction")
    if direction not in VALID_DIRECTIONS:
        errors.append(f"direction must be one of {VALID_DIRECTIONS}")
    paired = record.get("paired", False)
    if type(paired) is not bool:
        errors.append("paired must be a boolean when provided")
    min_effect_pct = record.get("min_effect_pct", 2.0)
    if not is_real_number(min_effect_pct) or float(min_effect_pct) < 0.0:
        errors.append("min_effect_pct must be a finite number >= 0")

    arm_lengths: dict[str, int] = {}
    for arm_name in ("baseline", "candidate"):
        arm = record.get(arm_name)
        if not isinstance(arm, dict):
            errors.append(f"{arm_name} must be an object with samples")
            continue
        arm_unit = arm.get("unit")
        if arm_unit is not None and arm_unit != record.get("unit"):
            errors.append(f"{arm_name}.unit does not match top-level unit")
        samples = arm.get("samples")
        if not isinstance(samples, list) or len(samples) < 3:
            errors.append(f"{arm_name}.samples must contain at least 3 numeric values")
            continue
        bad = [s for s in samples if not is_real_number(s) or float(s) <= 0.0]
        if bad:
            errors.append(f"{arm_name}.samples must contain only finite numbers > 0")
            continue
        arm_lengths[arm_name] = len(samples)

    if paired is True and len(arm_lengths) == 2 and arm_lengths["baseline"] != arm_lengths["candidate"]:
        errors.append("paired comparison requires equal baseline and candidate sample counts")
    return errors


def compare(record: dict[str, object], bootstrap_iters: int = DEFAULT_BOOTSTRAP_ITERS) -> dict[str, object]:
    direction = str(record["direction"])
    paired = bool(record.get("paired", False))
    min_effect_pct = float(record.get("min_effect_pct", 2.0))
    base_arm = record["baseline"]
    cand_arm = record["candidate"]
    assert isinstance(base_arm, dict) and isinstance(cand_arm, dict)
    base_samples = [float(x) for x in base_arm["samples"]]
    cand_samples = [float(x) for x in cand_arm["samples"]]

    base_stats = summarize(base_samples)
    cand_stats = summarize(cand_samples)
    base_med = float(base_stats["median"])
    cand_med = float(cand_stats["median"])

    if direction == "lower_is_better":
        speedup_ratio = base_med / cand_med
        pct_improvement = (base_med - cand_med) / base_med * 100.0
        paired_median_ratio = (
            quantile(sorted(b / c for b, c in zip(base_samples, cand_samples)), 0.50)
            if paired
            else None
        )
    else:
        speedup_ratio = cand_med / base_med
        pct_improvement = (cand_med - base_med) / base_med * 100.0
        paired_median_ratio = (
            quantile(sorted(c / b for b, c in zip(base_samples, cand_samples)), 0.50)
            if paired
            else None
        )

    ci_low, ci_high = bootstrap_ratio_ci(
        base_samples, cand_samples, direction, paired, bootstrap_iters
    )
    delta = cliffs_delta(base_samples, cand_samples, direction)
    u_stat, p_val = mann_whitney_u(base_samples, cand_samples)

    improve_floor = 1.0 + (min_effect_pct / 100.0)
    regress_ceiling = 1.0 / improve_floor
    if ci_low >= improve_floor:
        verdict = "SIGNIFICANT_IMPROVEMENT"
    elif ci_high <= regress_ceiling:
        verdict = "SIGNIFICANT_REGRESSION"
    else:
        verdict = "INDISTINGUISHABLE_FROM_NOISE"

    warnings: list[str] = []
    if min(len(base_samples), len(cand_samples)) < 7:
        warnings.append("Fewer than 7 samples per arm; statistical power for small effects is limited.")

    return {
        "schema_version": 1,
        "metric": record["metric"],
        "unit": record["unit"],
        "direction": direction,
        "paired": paired,
        "min_effect_pct": min_effect_pct,
        "baseline": {
            "label": base_arm.get("label", "baseline"),
            **base_stats,
        },
        "candidate": {
            "label": cand_arm.get("label", "candidate"),
            **cand_stats,
        },
        "speedup_ratio": speedup_ratio,
        "paired_median_ratio": paired_median_ratio,
        "pct_improvement": pct_improvement,
        "bootstrap_95ci": [ci_low, ci_high],
        "bootstrap_iters": bootstrap_iters,
        "cliffs_delta": delta,
        "mann_whitney_u": u_stat,
        "mann_whitney_p_approx": p_val,
        "verdict": verdict,
        "warnings": warnings,
        "disclaimer": (
            "Statistical comparison computed over recorded samples; hardware isolation, "
            "output equivalence, and execution provenance are not attested by this script."
        ),
    }


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError("Nonstandard JSON constant")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Statistical A/B benchmark comparator with nonparametric CI and noise-floor gating"
    )
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--bootstrap-iters", type=int, default=DEFAULT_BOOTSTRAP_ITERS)
    parser.add_argument("--fail-on-regression", action="store_true")
    parser.add_argument("--require-improvement", action="store_true")
    args = parser.parse_args()

    if args.bootstrap_iters < 200:
        print("bootstrap-iters must be >= 200", file=sys.stderr)
        return 1

    try:
        with args.record.open(encoding="utf-8") as stream:
            record = json.load(
                stream, object_pairs_hook=unique_object, parse_constant=reject_constant
            )
    except (OSError, ValueError, RecursionError) as exc:
        print(f"Benchmark record unavailable or invalid ({type(exc).__name__})", file=sys.stderr)
        return 1

    errors = validate_record(record)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    assert isinstance(record, dict)
    result = compare(record, bootstrap_iters=args.bootstrap_iters)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        ci = result["bootstrap_95ci"]
        base = result["baseline"]
        cand = result["candidate"]
        print(
            f"{result['metric']} ({result['unit']}, {result['direction']}, "
            f"{'paired' if result['paired'] else 'unpaired'}): {result['verdict']}"
        )
        print(
            f"  baseline  [{base['label']}]: n={base['n']} median={base['median']:.4g} "
            f"iqr={base['iqr']:.4g} mad={base['mad']:.4g} p99={base['p99']:.4g}"
        )
        print(
            f"  candidate [{cand['label']}]: n={cand['n']} median={cand['median']:.4g} "
            f"iqr={cand['iqr']:.4g} mad={cand['mad']:.4g} p99={cand['p99']:.4g}"
        )
        print(
            f"  speedup={result['speedup_ratio']:.4f}x ({result['pct_improvement']:+.2f}%) "
            f"95%CI=[{ci[0]:.4f}x, {ci[1]:.4f}x] cliffs_delta={result['cliffs_delta']:+.3f} "
            f"mwu_p={result['mann_whitney_p_approx']:.4g}"
        )
        for warn in result["warnings"]:
            print(f"  warning: {warn}")
        print(f"  note: {result['disclaimer']}")

    verdict = result["verdict"]
    if args.require_improvement and verdict != "SIGNIFICANT_IMPROVEMENT":
        return 2
    if args.fail_on_regression and verdict == "SIGNIFICANT_REGRESSION":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
