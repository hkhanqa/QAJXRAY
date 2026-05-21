pipeline {
    agent any

    environment {
        JIRA_PROJECT_KEY = 'QA'
        STORY_KEY        = 'QA-38'
        JIRA_DOMAIN      = 'hykhan.atlassian.net'
    }

    stages {

        stage('Clean Workspace') {
            steps { deleteDir() }
        }

        stage('Checkout Code') {
            steps {
                powershell '''
                    $ProgressPreference = "SilentlyContinue"
                    Invoke-WebRequest -Uri "https://github.com/hkhanqa/QAJXRAY/archive/refs/heads/main.zip" -OutFile "repo.zip"
                    Expand-Archive repo.zip -DestinationPath .
                    Move-Item QAJXRAY-main/* . -Force
                    Remove-Item repo.zip
                '''
            }
        }

        stage('Setup Python') {
            steps {
                powershell '''
                    python -m venv .venv
                    .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .\\.venv\\Scripts\\python.exe -m pip install selenium webdriver-manager requests unittest-xml-reporting
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    New-Item -ItemType Directory -Force -Path reports | Out-Null
                    .\\.venv\\Scripts\\python.exe test_login.py
                '''
            }
        }

        stage('Publish JUnit') {
            steps { junit 'reports/*.xml' }
        }

        /* ---------------------------------------------------------
           CREATE TEST SET
        --------------------------------------------------------- */
        stage('Create Test Set') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_EMAIL', passwordVariable: 'JIRA_API_TOKEN')]) {
                    powershell '''
                        $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:JIRA_EMAIL`:$env:JIRA_API_TOKEN"))

                        $body = @{
                            fields = @{
                                project   = @{ key = "$env:JIRA_PROJECT_KEY" }
                                summary   = "Automated Test Set for Story $env:STORY_KEY"
                                issuetype = @{ name = "Test Set" }
                            }
                        } | ConvertTo-Json -Depth 10

                        $resp = Invoke-RestMethod `
                            -Uri "https://$env:JIRA_DOMAIN/rest/api/3/issue" `
                            -Headers @{ Authorization = "Basic $auth"; "Content-Type"="application/json" } `
                            -Method Post `
                            -Body $body

                        $resp.key | Out-File -FilePath "testset.key" -Encoding ascii -NoNewline
                        Write-Host "Created Test Set: $($resp.key)"
                    '''
                }
            }
        }

        /* ---------------------------------------------------------
           EXTRACT TEST NAMES
        --------------------------------------------------------- */
        stage('Extract Test Names') {
            steps {
                powershell '''
                    $names = @()

                    Get-ChildItem "reports\\*.xml" | ForEach-Object {
                        [xml]$xml = Get-Content $_.FullName
                        foreach ($tc in $xml.testsuite.testcase) {
                            if ($tc.name) { $names += $tc.name }
                        }
                    }

                    $names = $names | Sort-Object -Unique
                    Write-Host "Detected Test Names: $names"

                    ($names -join ",") | Out-File -FilePath "detected_tests.name" -Encoding ascii -NoNewline
                '''
            }
        }

        /* ---------------------------------------------------------
           CREATE OR REUSE JIRA TESTS (NO DUPLICATES)
        --------------------------------------------------------- */
        stage('Create Jira Tests for Each Method') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_EMAIL', passwordVariable: 'JIRA_API_TOKEN')]) {
                    powershell '''
                        $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:JIRA_EMAIL`:$env:JIRA_API_TOKEN"))
                        $names = (Get-Content "detected_tests.name").Split(",") | ForEach-Object { $_.Trim() }
                        $keys  = @()

                        foreach ($name in $names) {

                            Write-Host "Checking if Test already exists EXACTLY: $name"

                            # EXACT MATCH JQL (PowerShell-safe quoting)
                            $jqlString = "summary = `"$name`" AND issuetype = Test"
                            $jql = [uri]::EscapeDataString($jqlString)
                            $searchUrl = "https://$env:JIRA_DOMAIN/rest/api/3/search?jql=$jql&fields=key"

                            $existingKey = $null

                            try {
                                $searchResp = Invoke-RestMethod -Uri $searchUrl -Headers @{ Authorization = "Basic $auth" } -Method Get
                                if ($searchResp.issues.Count -gt 0) {
                                    $existingKey = $searchResp.issues[0].key
                                }
                            } catch {}

                            if ($existingKey) {
                                Write-Host "Reusing existing Test: $existingKey"
                                $keys += $existingKey
                                continue
                            }

                            Write-Host "Creating NEW Test for: $name"

                            $body = @{
                                fields = @{
                                    project   = @{ key = "$env:JIRA_PROJECT_KEY" }
                                    summary   = $name
                                    issuetype = @{ name = "Test" }
                                }
                            } | ConvertTo-Json -Depth 10

                            $resp = Invoke-RestMethod `
                                -Uri "https://$env:JIRA_DOMAIN/rest/api/3/issue" `
                                -Headers @{ Authorization = "Basic $auth"; "Content-Type"="application/json" } `
                                -Method Post `
                                -Body $body

                            $keys += $resp.key
                        }

                        ($keys -join ",") | Out-File -FilePath "detected_tests.key" -Encoding ascii -NoNewline
                        Write-Host "Final Test Keys (deduped): $keys"
                    '''
                }
            }
        }

        /* ---------------------------------------------------------
           ADD TESTS TO TEST SET
        --------------------------------------------------------- */
        stage('Add Tests to Test Set') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_EMAIL', passwordVariable: 'JIRA_API_TOKEN'),
                    usernamePassword(credentialsId: 'xray-user-pass', usernameVariable: 'XRAY_CLIENT_ID', passwordVariable: 'XRAY_CLIENT_SECRET')
                ]) {
                    powershell '''
                        function Get-IssueId([string]$key) {
                            $url = "https://$($env:JIRA_DOMAIN)/rest/api/3/issue/$($key)?fields=id"
                            $resp = Invoke-RestMethod -Uri $url -Headers @{ Authorization = "Basic $jiraAuth" } -Method Get
                            return $resp.id
                        }

                        $testSetKey = (Get-Content "testset.key").Trim()
                        $testKeys   = (Get-Content "detected_tests.key").Split(",") | ForEach-Object { $_.Trim() }

                        $jiraAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:JIRA_EMAIL`:$env:JIRA_API_TOKEN"))
                        $testSetId = Get-IssueId $testSetKey
                        $testIds   = @()
                        foreach ($k in $testKeys) { if ($k) { $testIds += (Get-IssueId $k) } }

                        $authBody = @{ client_id = "$env:XRAY_CLIENT_ID"; client_secret = "$env:XRAY_CLIENT_SECRET" } | ConvertTo-Json
                        $token = Invoke-RestMethod -Uri "https://xray.cloud.getxray.app/api/v2/authenticate" -Method Post -Body $authBody -ContentType "application/json"
                        $token = $token.Replace('"','')
                        $headers = @{ Authorization = "Bearer $token" }

                        $idsList = ($testIds | ForEach-Object { "`"$($_)`"" }) -join ","
                        $mutation = @"
mutation {
  addTestsToTestSet(
    issueId: "$testSetId",
    testIssueIds: [$idsList]
  ) {
    addedTests
  }
}
"@
                        $body = @{ query = $mutation } | ConvertTo-Json
                        Invoke-RestMethod -Uri "https://xray.cloud.getxray.app/api/v2/graphql" -Method Post -Headers $headers -Body $body -ContentType "application/json"
                    '''
                }
            }
        }

        /* ---------------------------------------------------------
           CREATE TEST EXECUTION
        --------------------------------------------------------- */
        stage('Create Test Execution') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_EMAIL', passwordVariable: 'JIRA_API_TOKEN')]) {
                    powershell '''
                        $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:JIRA_EMAIL`:$env:JIRA_API_TOKEN"))
                        $body = @{
                            fields = @{
                                project   = @{ key = "$env:JIRA_PROJECT_KEY" }
                                summary   = "Automated Execution for $env:STORY_KEY"
                                issuetype = @{ name = "Test Execution" }
                            }
                        } | ConvertTo-Json -Depth 10
                        $resp = Invoke-RestMethod -Uri "https://$env:JIRA_DOMAIN/rest/api/3/issue" -Headers @{ Authorization = "Basic $auth"; "Content-Type"="application/json" } -Method Post -Body $body
                        $resp.key | Out-File -FilePath "execution.key" -Encoding ascii -NoNewline
                    '''
                }
            }
        }

        /* ---------------------------------------------------------
           LINK TESTS TO TEST EXECUTION
        --------------------------------------------------------- */
        stage('Link Tests to Test Execution') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_EMAIL', passwordVariable: 'JIRA_API_TOKEN'),
                    usernamePassword(credentialsId: 'xray-user-pass', usernameVariable: 'XRAY_CLIENT_ID', passwordVariable: 'XRAY_CLIENT_SECRET')
                ]) {
                    powershell '''
                        function Get-IssueId([string]$key) {
                            $url = "https://$($env:JIRA_DOMAIN)/rest/api/3/issue/$($key)?fields=id"
                            $resp = Invoke-RestMethod -Uri $url -Headers @{ Authorization = "Basic $jiraAuth" } -Method Get
                            return $resp.id
                        }

                        $executionKey = (Get-Content "execution.key").Trim()
                        $testKeys     = (Get-Content "detected_tests.key").Split(",") | ForEach-Object { $_.Trim() }

                        $jiraAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:JIRA_EMAIL`:$env:JIRA_API_TOKEN"))
                        $executionId = Get-IssueId $executionKey
                        $testIds     = @()
                        foreach ($k in $testKeys) { if ($k) { $testIds += (Get-IssueId $k) } }

                        $authBody = @{ client_id = "$env:XRAY_CLIENT_ID"; client_secret = "$env:XRAY_CLIENT_SECRET" } | ConvertTo-Json
                        $token = Invoke-RestMethod -Uri "https://xray.cloud.getxray.app/api/v2/authenticate" -Method Post -Body $authBody -ContentType "application/json"
                        $token = $token.Replace('"','')
                        $headers = @{ Authorization = "Bearer $token" }

                        $idsList = ($testIds | ForEach-Object { "`"$($_)`"" }) -join ","
                        $mutation = @"
mutation {
  addTestsToTestExecution(
    issueId: "$executionId",
    testIssueIds: [$idsList]
  ) {
    addedTests
  }
}
"@
                        $body = @{ query = $mutation } | ConvertTo-Json
                        Invoke-RestMethod -Uri "https://xray.cloud.getxray.app/api/v2/graphql" -Method Post -Headers $headers -Body $body -ContentType "application/json"
                    '''
                }
            }
        }

        /* ---------------------------------------------------------
           UPLOAD RESULTS TO XRAY CLOUD
        --------------------------------------------------------- */
        stage('Upload Results to Xray Cloud') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'xray-user-pass', usernameVariable: 'XRAY_CLIENT_ID', passwordVariable: 'XRAY_CLIENT_SECRET')]) {
                    powershell '''
                        $file = Get-ChildItem "reports\\*.xml" | Select-Object -First 1
                        $executionKey = (Get-Content "execution.key").Trim()

                        $authBody = @{ client_id = "$env:XRAY_CLIENT_ID"; client_secret = "$env:XRAY_CLIENT_SECRET" } | ConvertTo-Json
                        $token = Invoke-RestMethod -Uri "https://xray.cloud.getxray.app/api/v2/authenticate" -Method Post -Body $authBody -ContentType "application/json"
                        $token = $token.Replace('"','')
                        $headers = @{ Authorization = "Bearer $token" }

                        Invoke-RestMethod `
                            -Uri "https://xray.cloud.getxray.app/api/v2/import/execution/junit?testExecKey=$executionKey" `
                            -Method Post `
                            -Headers $headers `
                            -ContentType "text/xml" `
                            -InFile $file.FullName
                    '''
                }
            }
        }

        /* ---------------------------------------------------------
           LINK TEST EXECUTION → STORY
        --------------------------------------------------------- */
        stage('Link Test Execution to Story') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_EMAIL', passwordVariable: 'JIRA_API_TOKEN')]) {
                    powershell '''
                        $executionKey = (Get-Content "execution.key").Trim()

                        $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$env:JIRA_EMAIL`:$env:JIRA_API_TOKEN"))

                        $body = @{
                            type = @{ name = "Relates" }
                            inwardIssue  = @{ key = $executionKey }
                            outwardIssue = @{ key = "$env:STORY_KEY" }
                        } | ConvertTo-Json -Depth 10

                        Invoke-RestMethod `
                            -Uri "https://$env:JIRA_DOMAIN/rest/api/3/issueLink" `
                            -Headers @{ Authorization = "Basic $auth"; "Content-Type"="application/json" } `
                            -Method Post `
                            -Body $body
                    '''
                }
            }
        }
    }

    post {
        always  { echo "Pipeline completed" }
        success { echo "SUCCESS" }
        failure { echo "FAILED" }
    }
}
