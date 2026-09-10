#!/usr/bin/env python3
"""Create a small, repeatable IT-support project for the current Saturday."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECTS = [
    {
        "slug": "help-desk-triage",
        "title": "Help-desk ticket triage",
        "summary": "Define a consistent way to classify, prioritize, and escalate support requests.",
        "tasks": [
            "Create categories for hardware, software, access, network, and security requests.",
            "Set priority criteria based on user impact and business urgency.",
            "Write a short escalation path for unresolved or security-sensitive tickets.",
            "Review the process with one teammate and record one improvement.",
        ],
        "deliverable": "A one-page triage guide and an example ticket queue.",
    },
    {
        "slug": "device-inventory-audit",
        "title": "Device inventory audit",
        "summary": "Build a lightweight process for checking that assigned devices are documented and healthy.",
        "tasks": [
            "List the fields needed for each device: owner, asset tag, OS, location, and status.",
            "Check five sample devices for missing or outdated information.",
            "Document how to report a lost, retired, or reassigned device.",
            "Record one recommendation to improve inventory accuracy.",
        ],
        "deliverable": "A completed sample inventory and an audit checklist.",
    },
    {
        "slug": "backup-recovery-check",
        "title": "Backup and recovery check",
        "summary": "Verify that a small team knows what is backed up and how to recover a critical file.",
        "tasks": [
            "Identify one important folder and its backup location.",
            "Confirm the latest successful backup date without exposing private data.",
            "Perform a safe recovery of a non-sensitive test file.",
            "Document who to contact when recovery fails.",
        ],
        "deliverable": "A recovery runbook with the test result and follow-up actions.",
    },
    {
        "slug": "security-awareness-mini-session",
        "title": "Security-awareness mini-session",
        "summary": "Prepare a short, practical lesson on spotting phishing and reporting it safely.",
        "tasks": [
            "Collect three red flags that are easy for non-technical users to recognize.",
            "Write a safe reporting procedure that does not require clicking the message.",
            "Create a five-question knowledge check.",
            "Share the lesson with a teammate and capture feedback.",
        ],
        "deliverable": "A five-minute awareness handout and knowledge check.",
    },
]


def main() -> None:
    # Singapore is UTC+8 year-round, so this avoids requiring an external tzdata package.
    now = datetime.now(timezone(timedelta(hours=8)))
    date = now.date().isoformat()
    week = now.isocalendar().week
    project = PROJECTS[(week - 1) % len(PROJECTS)]
    folder = Path("projects") / f"{date}-{project['slug']}"
    folder.mkdir(parents=True, exist_ok=True)

    readme = f"# {project['title']}\n\n"
    readme += f"**Week of {date}**  \n"
    readme += f"{project['summary']}\n\n"
    readme += "## Objective\n\n"
    readme += "Practice a small, realistic support workflow that can be completed, reviewed, and improved in one week.\n\n"
    readme += "## Checklist\n\n"
    readme += "\n".join(f"- [ ] {task}" for task in project["tasks"])
    readme += f"\n\n## Deliverable\n\n{project['deliverable']}\n"
    readme += "\n## Notes\n\n- Do not include passwords, personal data, or production secrets in this project.\n"
    (folder / "README.md").write_text(readme, encoding="utf-8")

    checklist = "# Work log\n\n| Date | Owner | Result | Follow-up |\n|---|---|---|---|\n|  |  |  |  |\n"
    (folder / "work-log.md").write_text(checklist, encoding="utf-8")


if __name__ == "__main__":
    main()
