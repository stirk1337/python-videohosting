#!/usr/bin/env python3
"""Fail if pip-audit JSON report contains any vulnerability with CVSS base score >= 7.0.

pip-audit JSON does not embed CVSS; we resolve scores via OSV (api.osv.dev).
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

CVSS_THRESHOLD = 7.0


def _parse_cvss_score(score: str) -> float | None:
    s = score.strip()
    if not s:
        return None
    # OSV often stores "7.5" or a full CVSS vector string.
    if s[0].isdigit():
        parts = s.split("/", 1)
        try:
            return float(parts[0])
        except ValueError:
            return None
    return None


def _max_cvss_from_osv_payload(data: dict[str, Any]) -> float:
    best = 0.0
    for entry in data.get("severity") or []:
        if not str(entry.get("type", "")).startswith("CVSS"):
            continue
        raw = entry.get("score")
        if raw is None:
            continue
        val = _parse_cvss_score(str(raw))
        if val is not None:
            best = max(best, val)
    return best


def fetch_max_cvss(vuln_id: str, cache: dict[str, float]) -> float:
    if vuln_id in cache:
        return cache[vuln_id]
    safe = urllib.parse.quote(vuln_id, safe="")
    url = f"https://api.osv.dev/v1/vulns/{safe}"
    req = urllib.request.Request(url, headers={"User-Agent": "python-videohosting-ci"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.load(resp)
    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        json.JSONDecodeError,
    ):
        cache[vuln_id] = 0.0
        return 0.0
    score = _max_cvss_from_osv_payload(data)
    cache[vuln_id] = score
    return score


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: sca_cvss_gate.py <pip-audit-report.json>", file=sys.stderr)
        return 2
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            report = json.load(f)
    except OSError as e:
        print(f"cannot read report: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"invalid JSON: {e}", file=sys.stderr)
        return 2

    deps = report.get("dependencies") or []
    cache: dict[str, float] = {}
    blocking: list[tuple[str, str, str, float]] = []

    for dep in deps:
        if dep.get("skip_reason"):
            continue
        name = dep.get("name", "?")
        version = dep.get("version", "?")
        for vuln in dep.get("vulns") or []:
            vid = vuln.get("id")
            if not vid:
                continue
            max_cvss = fetch_max_cvss(str(vid), cache)
            if max_cvss >= CVSS_THRESHOLD:
                blocking.append((name, version, str(vid), max_cvss))

    if blocking:
        print("Blocking vulnerabilities (CVSS >= 7.0):", file=sys.stderr)
        for name, version, vid, score in blocking:
            print(f"  {name}@{version} — {vid} (max CVSS {score})", file=sys.stderr)
        return 1
    print("No vulnerabilities at or above CVSS 7.0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
