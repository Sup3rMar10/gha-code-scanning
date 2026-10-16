# gha-code-scanning

Two automatic security gates on GitHub: **CodeQL code scanning** finds vulnerabilities in the code, and **dependency review** blocks a pull request that adds a known-vulnerable package.

The first commit contains a **deliberately vulnerable** Flask app (command injection and SQL injection). Do not reuse it. The current `app/server.py` is the fixed version.

## What ran (2026-10-16)

**CodeQL, the full find-and-fix loop:**
- On the vulnerable commit, CodeQL reported 2 alerts in the Security tab: `py/sql-injection` (line 22) and `py/command-line-injection` (line 14).
- After the fix commit (no shell and list arguments with `--` plus input validation for the command, a parameterized query for SQL), both alerts moved to **fixed**.

**Dependency review, with a gotcha worth knowing:**
- Test pull requests (#1 and #2, both closed unmerged) changed `flask==3.0.3` to `flask==0.12.2`.
- The first attempts failed with `Dependency review is not supported on this repository. Please ensure that Dependency graph is enabled`. That was a **setup failure, not a finding**: the graph for a brand-new repo was not ready yet. (I also called the vulnerability-alerts API; I cannot say whether that call or just the passing of time fixed it.)
- After the graph was available, re-running blocked the pull request: `flask@0.12.2 - Flask is vulnerable to Denial of Service via incorrect encoding of JSON data (high severity)`, advisory GHSA-562c-5r94-xh97.

## Decisions

- **`security-events: write` only on the analyze job**; `persist-credentials: false` on checkout.
- **`fail-on-severity: moderate`** for dependency review: a policy choice, tune per customer.
- **Both scan on pull requests**, so problems are caught before merge, not after.
- **Why scanners are not enough:** they find known patterns; they do not replace review, and they produce false positives that need triage.

## Honest limits

- Default CodeQL query set, Python only; no alert triage, dismissal or SLA process.
- The fix for the ping endpoint is minimal; real code would avoid shelling out to `ping` at all.
- Code scanning is free on public repositories; private ones need GitHub Advanced Security.
- The vulnerable version stays in git history on purpose.

MIT licensed.
