# Backup restore and recovery-readiness test

**Week of 2026-10-03**  
Test a documented restore path and capture evidence against recovery-point and recovery-time objectives.

## Scenario

A finance share is classified as critical; the service owner has a 24-hour RPO and 4-hour RTO.

## Objective

Practice a small, realistic support workflow that can be completed, reviewed, and improved in one week.

## Checklist

- [ ] Record the system owner, backup policy, retention, RPO, RTO, and last successful job timestamp.
- [ ] Restore a non-sensitive test file to an isolated location and verify integrity.
- [ ] Time the exercise, capture evidence, and note dependencies or approval gates.
- [ ] Update the runbook with failure escalation, communications, and corrective actions.

## Deliverable

A restore evidence pack and recovery runbook mapped to RPO/RTO targets.


## Success measure

Test restore completes within the 4-hour RTO and identifies any RPO or evidence gap.

## Notes

- Do not include passwords, personal data, or production secrets in this project.
