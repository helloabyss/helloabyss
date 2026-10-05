"""State credit reporting law plug-ins.

Only states whose provisions have been checked are encoded. The case's state comes from
the consumer's current address. Add a state by appending to STATE_LAWS with sources.
"""

STATE_LAWS = {
    "CA": {
        "name": "California Consumer Credit Reporting Agencies Act (CCRAA)",
        "provisions": [
            ("Cal. Civ. Code § 1785.25(a)",
             "A furnisher may not furnish information it knows or should know is incomplete or "
             "inaccurate. Unlike FCRA § 1681s-2(a), this duty carries a private right of action "
             "(§§ 1785.25(g), 1785.31) that courts have held is not preempted by the FCRA."),
            ("Cal. Civ. Code § 1785.31",
             "Remedies: actual damages, fees and costs; punitive damages of $100-$5,000 per "
             "violation for willful violations."),
            ("Cal. Civ. Code § 1788 et seq. (Rosenthal Act)",
             "Applies FDCPA-style rules to original creditors collecting their own debts, not just "
             "third-party collectors."),
        ],
        "verified": "secondary (Justia/FindLaw code text, Ninth Circuit case law)",
    },
}


def state_notes(state):
    s = STATE_LAWS.get((state or "").upper())
    if not s:
        return (f"No state-law module encoded for {state or 'unknown state'}. Federal law still applies. "
                "Many states have their own credit reporting or collection statutes; check yours "
                "(or ask for that state's module to be added).")
    lines = [s["name"] + f"  [verified: {s['verified']}]"]
    lines += [f"  {cite}: {text}" for cite, text in s["provisions"]]
    return "\n".join(lines)
