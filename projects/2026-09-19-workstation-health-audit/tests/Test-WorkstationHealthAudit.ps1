$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $projectRoot 'Invoke-WorkstationHealthAudit.ps1'
$testOutput = Join-Path ([IO.Path]::GetTempPath()) ("workstation-audit-test-{0}" -f [guid]::NewGuid())

try {
    $result = & $scriptPath -OutputDirectory $testOutput
    if (-not (Test-Path -LiteralPath $result.JsonReport)) { throw 'JSON report was not created.' }
    if (-not (Test-Path -LiteralPath $result.HtmlReport)) { throw 'HTML report was not created.' }

    $report = Get-Content -LiteralPath $result.JsonReport -Raw | ConvertFrom-Json
    if ($report.SchemaVersion -ne '1.0') { throw 'Unexpected report schema version.' }
    if (-not $report.ComputerName) { throw 'Computer name is missing.' }
    if (@($report.Results).Count -lt 7) { throw 'One or more health checks are missing.' }

    $requiredFields = 'Check', 'Status', 'ObservedValue', 'Action'
    foreach ($checkResult in $report.Results) {
        foreach ($field in $requiredFields) {
            if ($null -eq $checkResult.$field) { throw "Result is missing required field: $field" }
        }
    }

    Write-Host "PASS: $(@($report.Results).Count) checks produced valid JSON and HTML reports."
}
finally {
    if (Test-Path -LiteralPath $testOutput) {
        Remove-Item -LiteralPath $testOutput -Recurse -Force
    }
}

