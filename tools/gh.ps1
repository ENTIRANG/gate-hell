# gh.ps1 — git 없이 GitHub와 주고받는 백업 도구
#
# 이 PC는 재시작하면 파일까지 초기화된다. git은 설치되어 있지 않고 설치해도 사라진다.
# 그래서 GitHub REST API를 HTTPS로 직접 호출한다. 설치도, 시스템 변경도 없다.
#
# 사용법:
#   .\tools\gh.ps1 save            # 프로젝트 전체를 커밋 1개로 올린다
#   .\tools\gh.ps1 save "메시지"    # 커밋 메시지 지정
#   .\tools\gh.ps1 load            # 리포 내용을 프로젝트 폴더로 내려받는다
#   .\tools\gh.ps1 status          # 설정과 최근 커밋 확인
#   .\tools\gh.ps1 token <값>      # 토큰 저장 (프로젝트 밖에 저장되므로 커밋되지 않는다)

param(
    [Parameter(Position = 0)][ValidateSet('save', 'load', 'status', 'token')]
    [string]$Action = 'status',
    [Parameter(Position = 1)][string]$Arg
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch { }

# ---------------------------------------------------------------- 설정

$Root = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $Root 'tools\repo.json'

# 토큰은 프로젝트 폴더 밖에 둔다. 실수로 커밋되는 일을 원천 차단한다.
$TokenPath = Join-Path $env:LOCALAPPDATA 'gate_hell_token.txt'

# 올리지 않을 것들 (repo.json 은 비밀이 아니고 복원에 필요하므로 올린다)
# 발표대본: 사용자가 커밋하지 말라고 지시함. 노션으로 옮겨 쓰는 임시 파일이다.
$Skip = @('__pycache__', '.git', '.vscode', '.pyc', '.pyo', 'token', '발표대본')

function Read-Config {
    if (-not (Test-Path $ConfigPath)) {
        throw "설정이 없습니다. tools\repo.json 을 만들고 owner/repo/branch 를 채우세요."
    }
    $c = Get-Content $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $c.owner -or $c.owner -eq '<USERNAME>') { throw "tools\repo.json 의 owner 를 GitHub 사용자명으로 바꾸세요." }
    if (-not $c.branch) { $c | Add-Member -NotePropertyName branch -NotePropertyValue 'main' -Force }
    return $c
}

function Read-Token {
    if (-not (Test-Path $TokenPath)) {
        throw "토큰이 없습니다.  .\tools\gh.ps1 token github_pat_xxxxx  로 먼저 저장하세요."
    }
    $t = (Get-Content $TokenPath -Raw -Encoding UTF8).Trim()
    if (-not $t) { throw "토큰 파일이 비어 있습니다." }
    return $t
}

function Invoke-GH {
    param([string]$Method, [string]$Path, $Body, [switch]$AllowMissing)

    $headers = @{
        'Authorization' = "Bearer $script:Token"
        'Accept'        = 'application/vnd.github+json'
        'User-Agent'    = 'gate-hell-backup'
    }
    $uri = "https://api.github.com$Path"
    try {
        if ($null -ne $Body) {
            $json = $Body | ConvertTo-Json -Depth 20 -Compress
            $bytes = [Text.Encoding]::UTF8.GetBytes($json)
            return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers -Body $bytes -ContentType 'application/json'
        }
        return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers
    }
    catch {
        $code = $null
        if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
        # 빈 리포는 ref 조회에 409(Git Repository is empty)를 낸다. 404 와 같이 "없음" 으로 본다.
        if ($AllowMissing -and ($code -eq 404 -or $code -eq 409)) { return $null }
        if ($code -eq 401) { throw "인증 실패(401). 토큰이 만료되었거나 잘못되었습니다. 새로 발급받으세요." }
        if ($code -eq 403) { throw "권한 없음(403). 토큰의 Contents 권한이 Read and write 인지 확인하세요." }
        if ($code -eq 404) { throw "찾을 수 없음(404). owner/repo 이름과 토큰의 리포 접근 범위를 확인하세요. ($Method $Path)" }
        throw "GitHub API 실패 ($code): $($_.Exception.Message)  [$Method $Path]"
    }
}

function Get-ProjectFiles {
    Get-ChildItem -Path $Root -Recurse -File -Force | Where-Object {
        $rel = $_.FullName.Substring($Root.Length + 1)
        $bad = $false
        foreach ($s in $Skip) { if ($rel -like "*$s*") { $bad = $true } }
        -not $bad
    }
}

function Get-RepoPath([IO.FileInfo]$f) {
    $rel = $f.FullName.Substring($Root.Length + 1)
    return $rel.Replace('\', '/')
}

# ---------------------------------------------------------------- 동작

switch ($Action) {

    'token' {
        if (-not $Arg) { throw "사용법: .\tools\gh.ps1 token github_pat_xxxxx" }
        Set-Content -Path $TokenPath -Value $Arg.Trim() -Encoding utf8 -NoNewline
        Write-Output "토큰 저장됨 -> $TokenPath"
        Write-Output "(프로젝트 폴더 밖이므로 커밋되지 않습니다. 재시작하면 사라집니다.)"
    }

    'status' {
        $cfg = Read-Config
        Write-Output "리포   : $($cfg.owner)/$($cfg.repo)  [$($cfg.branch)]"
        if (Test-Path $TokenPath) { Write-Output "토큰   : 저장됨" } else { Write-Output "토큰   : 없음  -> .\tools\gh.ps1 token <값>" ; break }
        $script:Token = Read-Token
        $br = Invoke-GH GET "/repos/$($cfg.owner)/$($cfg.repo)/branches/$($cfg.branch)" -AllowMissing
        if (-not $br) { Write-Output "커밋   : 없음 (빈 리포)" ; break }
        $commit = Invoke-GH GET "/repos/$($cfg.owner)/$($cfg.repo)/git/commits/$($br.commit.sha)"
        Write-Output "최근   : $($commit.message)"
        Write-Output "시각   : $($commit.committer.date)"
        Write-Output ""
        Write-Output "올릴 파일:"
        Get-ProjectFiles | ForEach-Object { "  {0,-28} {1,7} B" -f (Get-RepoPath $_), $_.Length }
    }

    'save' {
        $cfg = Read-Config
        $script:Token = Read-Token
        $msg = $Arg
        if (-not $msg) { $msg = 'backup' }
        $base = "/repos/$($cfg.owner)/$($cfg.repo)"

        $files = @(Get-ProjectFiles)
        if ($files.Count -eq 0) { throw "올릴 파일이 없습니다." }

        # 0. 빈 리포면 Git Data API 가 409 를 낸다. Contents API 로 씨앗 커밋을 먼저 만든다.
        $br = Invoke-GH GET "$base/branches/$($cfg.branch)" -AllowMissing
        if (-not $br) {
            $seed = $files[0]
            $seedPath = Get-RepoPath $seed
            Write-Output "빈 리포입니다. '$seedPath' 로 브랜치를 초기화합니다."
            Invoke-GH PUT "$base/contents/$seedPath" @{
                message = 'init'
                content = [Convert]::ToBase64String([IO.File]::ReadAllBytes($seed.FullName))
                branch  = $cfg.branch
            } | Out-Null
            $br = Invoke-GH GET "$base/branches/$($cfg.branch)"
        }
        $parent = $br.commit.sha
        if (-not $parent) { throw "브랜치 '$($cfg.branch)' 의 커밋 SHA를 읽지 못했습니다." }

        # 1. 각 파일을 blob 으로 업로드
        #    ArrayList 를 쓴다. $arr += @{...} 는 해시테이블 병합이 되어 키 충돌을 낸다.
        $tree = New-Object System.Collections.ArrayList
        foreach ($f in $files) {
            $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($f.FullName))
            $blob = Invoke-GH POST "$base/git/blobs" @{ content = $b64; encoding = 'base64' }
            [void]$tree.Add(@{ path = (Get-RepoPath $f); mode = '100644'; type = 'blob'; sha = $blob.sha })
            Write-Output "  + $(Get-RepoPath $f)"
        }

        # 2. base_tree 를 쓰지 않는다. 매번 전체 파일을 올리므로 트리를 통째로 새로 만든다.
        #    그래야 로컬에서 지우거나 옮긴 파일이 리포에도 그대로 반영된다.
        #    base_tree 를 쓰면 사라진 파일이 리포에 남는다.
        $treeBody = @{ tree = $tree }

        # 3. 트리 -> 커밋 -> 브랜치 이동
        $newTree = Invoke-GH POST "$base/git/trees" $treeBody
        $commit = Invoke-GH POST "$base/git/commits" @{ message = $msg; tree = $newTree.sha; parents = @($parent) }
        Invoke-GH PATCH "$base/git/refs/heads/$($cfg.branch)" @{ sha = $commit.sha } | Out-Null

        Write-Output ""
        Write-Output "커밋 완료: $($commit.sha.Substring(0,7))  `"$msg`"  ($($files.Count)개 파일)"
        Write-Output "https://github.com/$($cfg.owner)/$($cfg.repo)"
    }

    'load' {
        $cfg = Read-Config
        $script:Token = Read-Token
        $base = "/repos/$($cfg.owner)/$($cfg.repo)"

        $br = Invoke-GH GET "$base/branches/$($cfg.branch)" -AllowMissing
        if (-not $br) { throw "리포가 비어 있습니다. 내려받을 것이 없습니다." }
        $commit = Invoke-GH GET "$base/git/commits/$($br.commit.sha)"
        $tree = Invoke-GH GET "$base/git/trees/$($commit.tree.sha)?recursive=1"

        foreach ($item in $tree.tree) {
            if ($item.type -ne 'blob') { continue }
            $blob = Invoke-GH GET "$base/git/blobs/$($item.sha)"
            $bytes = [Convert]::FromBase64String($blob.content.Replace("`n", ''))
            $dest = Join-Path $Root ($item.path.Replace('/', '\'))
            $dir = Split-Path -Parent $dest
            if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
            [IO.File]::WriteAllBytes($dest, $bytes)
            Write-Output "  v $($item.path)"
        }
        Write-Output ""
        Write-Output "복원 완료: $($commit.message)  ($($commit.committer.date))"
    }
}
