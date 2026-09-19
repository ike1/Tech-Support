# Workstation health-audit automation

**Project date:** 2026-09-19  
**Function:** Collect repeatable endpoint-health evidence for IT support triage.

## Business case

Support technicians often collect the same workstation details manually before assigning or escalating a ticket. This implementation gathers a small, non-sensitive health snapshot and produces consistent JSON and HTML reports that can be attached to a ticket.

## What it checks

- Operating-system name, version, and build
- Uptime against a configurable maximum
- System-drive free space against a configurable minimum
- Available physical memory
- Pending Windows restart indicators
- Windows Defender service state
- Active physical network adapters

The tool does not collect passwords, browser data, user documents, product keys, or application content.

## Requirements

- Windows 10/11 or Windows Server
- Windows PowerShell 5.1 or PowerShell 7+
- No third-party modules or paid software
- Standard user access for most checks; inaccessible checks are reported as `Unknown`

## Run

Open PowerShell in this project directory:

```powershell
.\Invoke-WorkstationHealthAudit.ps1
```

Use custom thresholds and an output location:

```powershell
.\Invoke-WorkstationHealthAudit.ps1 `
  -OutputDirectory C:\ITSupport\HealthReports `
  -MinimumFreeDiskPercent 20 `
  -MaximumUptimeDays 14
```

The command creates one JSON report for integrations and one HTML report for technician review. It prints the paths and overall status when complete.

## Validate

The validation uses only PowerShell and writes temporary test output outside the repository:

```powershell
.\tests\Test-WorkstationHealthAudit.ps1
```

## Operational rollout

1. Test on one non-production workstation.
2. Review thresholds with endpoint and security owners.
3. Deploy through the approved endpoint-management tool, such as Intune, Configuration Manager, or an RMM platform.
4. Store reports only in an approved support location with normal ticket-retention controls.
5. Review warnings before remediation; this tool reports conditions and does not change the endpoint.

## Acceptance criteria

- Both report formats are produced without third-party dependencies.
- Every check contains a status, observed value, and technician action.
- Failed or inaccessible checks do not stop the remaining audit.
- The script makes no configuration changes to the workstation.

