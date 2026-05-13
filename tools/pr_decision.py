def decide_pr(coverage, ccn, status):

    reasons = []

    if coverage < 80:
        reasons.append("Coverage below threshold")

    if ccn > 15:
        reasons.append("High cyclomatic complexity")

    if status != "pass":
        reasons.append("Tests failed")

    if reasons:
        return {
            "decision": "REJECT",
            "reasons": reasons
        }

    return {
        "decision": "APPROVE",
        "reasons": ["All checks passed"]
    }
