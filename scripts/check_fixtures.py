#!/usr/bin/env python3
"""Check the evaluation manifest and observable behavior of a disposable fixture."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET


def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(f"{args!r} exited {result.returncode}:\n{result.stdout}{result.stderr}")
    return result.stdout


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_manifest(root):
    manifest = json.loads((root / "evals/evals.json").read_text())
    name = re.search(r"(?m)^name: ([a-z0-9-]+)$", (root / "SKILL.md").read_text())
    require(name and manifest["skill_name"] == name.group(1), "Manifest and skill names differ")
    cases = manifest["evals"]
    require(len({case["id"] for case in cases}) == len(cases), "Duplicate evaluation IDs")
    require(len({case["name"] for case in cases}) == len(cases), "Duplicate evaluation names")
    assertion_ids = []
    for case in cases:
        require(case["prompt"] and case["assertions"], f"Empty evaluation: {case['id']}")
        if "fixture" in case:
            require((root / "evals" / case["fixture"]).is_dir(), f"Missing fixture: {case['id']}")
        assertion_ids.extend(item["id"] for item in case["assertions"])
    require(len(set(assertion_ids)) == len(assertion_ids), "Duplicate assertion IDs")
    print(f"PASS: {len(cases)} evaluation cases have unique IDs and valid fixture paths")


def check_go(fixture):
    packages = run(["go", "list", "-f", "{{.ImportPath}} {{.Name}}", "./..."], fixture)
    require("example.com/docaudit docaudit" in packages, "Library package was not discovered")
    require("example.com/docaudit/cmd/cachectl main" in packages, "Command package was not discovered")
    events = [json.loads(line) for line in run(
        ["go", "test", "-json", "-run", "^Example", "-count=1", "./..."], fixture
    ).splitlines()]
    executed = {event.get("Test") for event in events if event["Action"] == "run"}
    passed = {event.get("Test") for event in events if event["Action"] == "pass"}
    require("ExampleLookup" in executed & passed, "ExampleLookup did not execute and pass")
    require("ExampleCache_Get" not in executed, "Compile-only example unexpectedly executed")
    print("PASS: Go discovers library + CLI; ExampleLookup runs; ExampleCache_Get is compile-only")


def check_ripwire(fixture):
    print(run(["ripwire", "--version"], fixture).strip())
    drift = ET.fromstring(run(["ripwire", ".", "--doc-drift=README.md"], fixture))
    findings = list(drift.iter("a"))
    require(any(row.get("why") == "const-value" and row.get("got") == "8" for row in findings),
            "Ripwire did not detect the planted constant mismatch")
    require(any(row.get("why") == "missing-file" for row in findings),
            "Ripwire did not detect the planted missing source file")
    comments = ET.fromstring(run(["ripwire", ".", "--comment-coherence"], fixture))
    scores = {row.get("n"): float(row.get("c_coeff")) for row in comments.iter("fn")}
    require("Set" in scores and "Get" in scores and scores["Set"] > scores["Get"],
            "Name-restating Set comment should rank above the informative Get comment")
    print("PASS: Ripwire detects seeded anchor drift and distinguishes comment restatement")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ripwire", action="store_true", help="also check installed Ripwire behavior")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    check_manifest(root)
    required = ["go"] + (["ripwire"] if args.ripwire else [])
    for binary in required:
        require(shutil.which(binary), f"Required tool unavailable: {binary}")
    with tempfile.TemporaryDirectory(prefix="golang-doc-ripwire-") as temp:
        fixture = Path(temp) / "doc-audit"
        shutil.copytree(root / "evals/fixtures/doc-audit", fixture)
        check_go(fixture)
        if args.ripwire:
            check_ripwire(fixture)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired, OSError, ValueError, ET.ParseError) as error:
        raise SystemExit(f"FAIL: {error}") from error
