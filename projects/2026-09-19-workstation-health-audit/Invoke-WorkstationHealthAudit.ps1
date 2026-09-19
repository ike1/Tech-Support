[CmdletBinding()]
param(
    [Parameter()]
    [ValidateRange(1, 99)]
    [int]$MinimumFreeDiskPercent = 15,

    [Parameter()]
    [ValidateRange(1, 365)]
    [int]$MaximumUptimeDays = 30,

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'reports')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function New-AuditResult {
    param(
        [string]$Check,
        [ValidateSet('Healthy', 'Warning', 'Unknown')]
        [string]$Status,
        [string]$ObservedValue,
        [string]$Action
    )

    [pscustomobject]@{
        Check         = $Check
        Status        = $Status
        ObservedValue = $ObservedValue
        Action        = $Action
    }
}

function Invoke-SafeCheck {
    param(
        [string]$Name,
        [scriptblock]$Operation
    )

    try {
        & $Operation
    }
    catch {
        New-AuditResult -Check $Name -Status Unknown -ObservedValue $_.Exception.Message `
            -Action 'Confirm permissions and collect this value manually.'
    }
}

$computerName = if ($env:COMPUTERNAME) { $env:COMPUTERNAME } else { [Environment]::MachineName }
$os = $null
$results = @()

$results += Invoke-SafeCheck -Name 'Operating system' -Operation {
    $script:os = Get-CimInstance -ClassName Win32_OperatingSystem
    $value = '{0}; version {1}; build {2}' -f $script:os.Caption, $script:os.Version, $script:os.BuildNumber
    New-AuditResult -Check 'Operating system' -Status Healthy -ObservedValue $value -Action 'No action required.'
}

$results += Invoke-SafeCheck -Name 'System uptime' -Operation {
    if (-not $script:os) {
        $script:os = Get-CimInstance -ClassName Win32_OperatingSystem
    }
    $uptime = (Get-Date) - $script:os.LastBootUpTime
    $status = if ($uptime.TotalDays -gt $MaximumUptimeDays) { 'Warning' } else { 'Healthy' }
    $action = if ($status -eq 'Warning') { 'Schedule a restart after confirming user impact and change requirements.' } else { 'No action required.' }
    New-AuditResult -Check 'System uptime' -Status $status `
        -ObservedValue ('{0:N1} days' -f $uptime.TotalDays) -Action $action
}

$results += Invoke-SafeCheck -Name 'System drive free space' -Operation {
    $systemDrive = if ($env:SystemDrive) { $env:SystemDrive.TrimEnd(':') } else { 'C' }
    $disk = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='$($systemDrive):'"
    if (-not $disk -or -not $disk.Size) { throw 'System drive information was unavailable.' }
    $freePercent = ($disk.FreeSpace / $disk.Size) * 100
    $status = if ($freePercent -lt $MinimumFreeDiskPercent) { 'Warning' } else { 'Healthy' }
    $action = if ($status -eq 'Warning') { 'Review approved cleanup options or increase storage capacity.' } else { 'No action required.' }
    New-AuditResult -Check 'System drive free space' -Status $status `
        -ObservedValue ('{0:N1}% free ({1:N1} GB)' -f $freePercent, ($disk.FreeSpace / 1GB)) -Action $action
}

$results += Invoke-SafeCheck -Name 'Available memory' -Operation {
    if (-not $script:os) {
        $script:os = Get-CimInstance -ClassName Win32_OperatingSystem
    }
    $availableGb = $script:os.FreePhysicalMemory * 1KB / 1GB
    $totalGb = $script:os.TotalVisibleMemorySize * 1KB / 1GB
    $availablePercent = ($availableGb / $totalGb) * 100
    $status = if ($availablePercent -lt 10) { 'Warning' } else { 'Healthy' }
    $action = if ($status -eq 'Warning') { 'Review high-memory processes and confirm the endpoint workload.' } else { 'No action required.' }
    New-AuditResult -Check 'Available memory' -Status $status `
        -ObservedValue ('{0:N1} GB of {1:N1} GB ({2:N1}%)' -f $availableGb, $totalGb, $availablePercent) -Action $action
}

$results += Invoke-SafeCheck -Name 'Pending restart' -Operation {
    $rebootKeys = @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
    )
    $pending = ($rebootKeys | Where-Object { Test-Path -LiteralPath $_ }).Count -gt 0
    $sessionManager = Get-ItemProperty -LiteralPath 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' `
        -Name PendingFileRenameOperations -ErrorAction SilentlyContinue
    $pending = $pending -or ($null -ne $sessionManager)
    $status = if ($pending) { 'Warning' } else { 'Healthy' }
    $action = if ($pending) { 'Schedule a restart after confirming user impact and change requirements.' } else { 'No action required.' }
    New-AuditResult -Check 'Pending restart' -Status $status -ObservedValue $pending.ToString() -Action $action
}

$results += Invoke-SafeCheck -Name 'Microsoft Defender service' -Operation {
    $service = Get-Service -Name WinDefend
    $status = if ($service.Status -eq 'Running') { 'Healthy' } else { 'Warning' }
    $action = if ($status -eq 'Warning') { 'Confirm the approved endpoint-protection product and escalate unexpected service state.' } else { 'No action required.' }
    New-AuditResult -Check 'Microsoft Defender service' -Status $status `
        -ObservedValue $service.Status.ToString() -Action $action
}

$results += Invoke-SafeCheck -Name 'Active network adapters' -Operation {
    $adapters = @(Get-CimInstance -ClassName Win32_NetworkAdapter -Filter 'NetEnabled=True' | Where-Object PhysicalAdapter)
    $status = if ($adapters.Count -gt 0) { 'Healthy' } else { 'Warning' }
    $value = if ($adapters.Count -gt 0) { ($adapters.Name -join '; ') } else { 'No active physical adapter found.' }
    $action = if ($status -eq 'Warning') { 'Check the physical connection, adapter state, and approved network configuration.' } else { 'No action required.' }
    New-AuditResult -Check 'Active network adapters' -Status $status -ObservedValue $value -Action $action
}

$overallStatus = if ($results.Status -contains 'Warning') { 'Attention required' } elseif ($results.Status -contains 'Unknown') { 'Review required' } else { 'Healthy' }
$timestamp = Get-Date
$report = [ordered]@{
    SchemaVersion = '1.0'
    ComputerName  = $computerName
    CollectedAt   = $timestamp.ToString('o')
    OverallStatus = $overallStatus
    Thresholds    = [ordered]@{
        MinimumFreeDiskPercent = $MinimumFreeDiskPercent
        MaximumUptimeDays      = $MaximumUptimeDays
    }
    Results       = $results
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$safeComputerName = $computerName -replace '[^A-Za-z0-9_.-]', '_'
$fileStem = '{0}-{1}' -f $safeComputerName, $timestamp.ToString('yyyyMMdd-HHmmss')
$jsonPath = Join-Path $OutputDirectory "$fileStem.json"
$htmlPath = Join-Path $OutputDirectory "$fileStem.html"

$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$style = @'
<style>
body { font-family: Arial, sans-serif; margin: 2rem; color: #202124; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #d0d7de; padding: 0.55rem; text-align: left; }
th { background: #f6f8fa; }
h1 { font-size: 1.5rem; }
</style>
'@
$preContent = "<h1>Workstation health audit</h1><p><strong>Computer:</strong> $computerName<br><strong>Collected:</strong> $($timestamp.ToString('u'))<br><strong>Overall status:</strong> $overallStatus</p>"
$results | ConvertTo-Html -Title "Health audit - $computerName" -Head $style -PreContent $preContent |
    Set-Content -LiteralPath $htmlPath -Encoding UTF8

[pscustomobject]@{
    OverallStatus = $overallStatus
    JsonReport    = $jsonPath
    HtmlReport    = $htmlPath
}

