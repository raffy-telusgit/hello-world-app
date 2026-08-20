"""Reads a trigger file describing a labeled GitHub issue, asks FueliX for a
recommendation grounded in this repo's kb/*.md articles, and posts the result
back as an issue comment. Runs as a Cloud Build step (see
cloudbuild-issue-triage.yaml) - never as a long-running service."""

import json
import os
import sys
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "kb"

FUELIX_BASE_URL = os.environ.get("FUELIX_BASE_URL", "https://api.fuelix.ai/v1")
FUELIX_MODEL = os.environ.get("FUELIX_MODEL", "claude-sonnet-4")
FUELIX_API_KEY = os.environ["FUELIX_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


def load_kb_docs() -> list[dict]:
    return [
        {"name": path.name, "content": path.read_text(encoding="utf-8")}
        for path in sorted(KB_DIR.glob("*.md"))
    ]


def build_prompt(issue_title: str, issue_body: str, kb_docs: list[dict]) -> list[dict]:
    kb_text = "\n\n".join(f"### {doc['name']}\n{doc['content']}" for doc in kb_docs) or "(no KB articles found)"
    system = (
        "You are an on-call triage assistant. You are given a GitHub issue and a set of "
        "internal knowledge-base articles. Recommend a concrete fix, citing which KB "
        "article(s) support it if any apply. If nothing in the KB applies, say so and give "
        "your best general recommendation. Keep the response under 200 words, formatted as "
        "GitHub-flavored markdown."
    )
    user = f"## Issue: {issue_title}\n\n{issue_body}\n\n## Knowledge base articles\n\n{kb_text}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_fuelix(messages: list[dict]) -> str:
    res = httpx.post(
        f"{FUELIX_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {FUELIX_API_KEY}", "Content-Type": "application/json"},
        json={"model": FUELIX_MODEL, "messages": messages},
        timeout=30,
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()


def post_comment(repo: str, issue_number: int, body: str) -> None:
    res = httpx.post(
        f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        json={"body": body},
        timeout=15,
    )
    res.raise_for_status()


def main() -> None:
    trigger_path = Path(sys.argv[1])
    trigger = json.loads(trigger_path.read_text(encoding="utf-8"))

    kb_docs = load_kb_docs()
    messages = build_prompt(trigger["issue_title"], trigger["issue_body"] or "", kb_docs)
    recommendation = call_fuelix(messages)

    comment = f"### \U0001f916 Issue Triage Agent\n\n{recommendation}"
    post_comment(trigger["repo"], trigger["issue_number"], comment)
    print(f"Posted triage recommendation on {trigger['repo']}#{trigger['issue_number']}")


if __name__ == "__main__":
    main()
