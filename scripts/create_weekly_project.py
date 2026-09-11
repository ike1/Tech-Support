#!/usr/bin/env python3
"""Create a small, repeatable, industry-relevant IT-support project."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECTS = [
    {
        "slug": "help-desk-triage",
        "title": "Help-desk triage and SLA workflow",
        "summary": "Design a service-desk workflow that routes incidents consistently and protects response-time commitments.",
        "context": "You support a 150-user organization with business-hours support and four priority levels.",
        "tasks": [
            "Map five common request types to an ITIL-style incident, service request, or access request category.",
            "Define P1-P4 impact/urgency rules, response targets, escalation owners, and an SLA-breach warning.",
            "Create three sanitized sample tickets with assignment group, customer updates, and closure codes.",
            "Review the workflow against a weekly ticket report and record one improvement.",
        ],
        "deliverable": "A triage decision tree, SLA matrix, and three sample tickets.",
        "metrics": "At least 90% of sample tickets are categorized and assigned correctly on first review.",
    },
    {
        "slug": "device-inventory-audit",
        "title": "Endpoint inventory and lifecycle audit",
        "summary": "Reconcile endpoint records with an asset register and identify lifecycle, patching, and ownership gaps.",
        "context": "You administer laptops through an MDM platform and need evidence for an internal control review.",
        "tasks": [
            "Define required CMDB fields: asset tag, serial number, owner, cost center, OS version, encryption, and lifecycle state.",
            "Reconcile ten sanitized records against MDM data and classify discrepancies by root cause.",
            "Document joiner, mover, leaver, lost-device, and secure-retirement handoffs.",
            "Prioritize remediation using risk, age, warranty status, and patch compliance.",
        ],
        "deliverable": "A reconciliation report, lifecycle RACI, and audit-ready checklist.",
        "metrics": "100% of sample assets have an owner and lifecycle state; all exceptions have an assigned action.",
    },
    {
        "slug": "backup-recovery-check",
        "title": "Backup restore and recovery-readiness test",
        "summary": "Test a documented restore path and capture evidence against recovery-point and recovery-time objectives.",
        "context": "A finance share is classified as critical; the service owner has a 24-hour RPO and 4-hour RTO.",
        "tasks": [
            "Record the system owner, backup policy, retention, RPO, RTO, and last successful job timestamp.",
            "Restore a non-sensitive test file to an isolated location and verify integrity.",
            "Time the exercise, capture evidence, and note dependencies or approval gates.",
            "Update the runbook with failure escalation, communications, and corrective actions.",
        ],
        "deliverable": "A restore evidence pack and recovery runbook mapped to RPO/RTO targets.",
        "metrics": "Test restore completes within the 4-hour RTO and identifies any RPO or evidence gap.",
    },
    {
        "slug": "security-awareness-mini-session",
        "title": "Phishing-reporting and incident handoff drill",
        "summary": "Run a controlled phishing-reporting exercise and improve the handoff from users to the security queue.",
        "context": "Your organization uses an email-report button and a central incident queue monitored by security operations.",
        "tasks": [
            "Prepare a clearly labeled, harmless simulation using approved test content; never collect credentials.",
            "Define the user reporting steps, analyst triage fields, evidence preservation, and containment handoff.",
            "Measure report rate, false positives, and time from report to analyst acknowledgement.",
            "Publish a five-minute refresher and capture lessons learned with the security team.",
        ],
        "deliverable": "An approved exercise plan, handoff checklist, and metrics summary.",
        "metrics": "Every simulated report reaches the security queue with required fields and no real user data collected.",
    },
    {
        "slug": "access-review",
        "title": "Quarterly access-review remediation",
        "summary": "Review privileged and leaver access, document approvals, and close exceptions with evidence.",
        "context": "You are preparing evidence for a quarterly least-privilege and joiner/mover/leaver control.",
        "tasks": [
            "Export a sanitized sample of application and group memberships with manager and system-owner fields.",
            "Identify dormant accounts, excessive privilege, and leaver access; do not disable production users in this exercise.",
            "Route exceptions for owner approval and record due dates, compensating controls, and closure evidence.",
            "Summarize completion rate and overdue risk for the service owner.",
        ],
        "deliverable": "An access-review worksheet, exception register, and owner-ready summary.",
        "metrics": "100% of sampled privileged accounts have a current owner decision and evidence link.",
    },
    {
        "slug": "knowledge-base-improvement",
        "title": "Knowledge-base article and deflection improvement",
        "summary": "Turn a repeat support issue into a tested knowledge article that reduces avoidable tickets.",
        "context": "Password-reset and VPN tickets are among the top recurring contacts in the service desk.",
        "tasks": [
            "Use sanitized ticket data to select one high-volume, low-risk issue and identify its root cause.",
            "Write a user-facing article with prerequisites, screenshots or commands, accessibility, and rollback guidance.",
            "Have a non-technical colleague follow the article and record time-to-resolution and confusion points.",
            "Publish a review cadence, owner, feedback path, and deflection measurement.",
        ],
        "deliverable": "A tested knowledge-base article with review metadata and baseline metric.",
        "metrics": "A tester completes the procedure without technician intervention and all steps are reproducible.",
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
    readme += f"## Scenario\n\n{project['context']}\n\n"
    readme += "## Objective\n\n"
    readme += "Practice a small, realistic support workflow that can be completed, reviewed, and improved in one week.\n\n"
    readme += "## Checklist\n\n"
    readme += "\n".join(f"- [ ] {task}" for task in project["tasks"])
    readme += f"\n\n## Deliverable\n\n{project['deliverable']}\n"
    readme += f"\n\n## Success measure\n\n{project['metrics']}\n"
    readme += "\n## Notes\n\n- Do not include passwords, personal data, or production secrets in this project.\n"
    (folder / "README.md").write_text(readme, encoding="utf-8")

    checklist = "# Work log\n\n| Date | Owner | Result | Follow-up |\n|---|---|---|---|\n|  |  |  |  |\n"
    (folder / "work-log.md").write_text(checklist, encoding="utf-8")


if __name__ == "__main__":
    main()
