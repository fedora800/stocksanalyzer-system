pipeline {
  agent any
    
  environment {

    //WEBHOOK_SECRET_FOR_GITHUB = credentials('cred_jenkins_token_for_github') // Jenkins secret credential ID setup for this github webhook
    GIT_USER_NAME = "fedora800"

    APP_GIT_REPO_NAME = "stocksanalyzer-system"
    APP_GIT_REPO_URL = "https://github.com/fedora800/stocksanalyzer-system.git"
    APP_GIT_REPO_BRANCH = "main"
    APP_GIT_CREDENTIALS_ID = "cred-github-fedora800-PAT"

    APP_GITOPS_REPO_NAME = "gitops-stocksanalyzer-system"
    APP_GITOPS_REPO_URL = 'https://github.com/fedora800/gitops-stocksanalyzer-system.git' 
    APP_GITOPS_BRANCH = 'main'
    APP_GITOPS_CREDENTIALS_ID = 'cred-github-fedora800-PAT'

    DEPLOYMENT_YAML_FILE = 'kubernetes-manifests/frontend/dpl-frontend.yaml'
    SERVICE_YAML_FILE = 'kubernetes-manifests/frontend/svc-frontend.yaml'


    REPO_URL = "${env.repo_url}"
    REF = "${env.ref}"
    BRANCH = REF.replaceAll('^refs/heads/', '')
    RELEASE = BRANCH.replaceAll('^.*/', '')
    VERSION = RELEASE.replaceAll('^v', '')


      APP_NAME = "stocksanalyzer-frontend-app"
      APP_VERSION_PREFIX = "1.0"            // currently hardcoding till i find solution to maybe get from build config or somewhere else
      APP_VERSION = "${APP_VERSION_PREFIX}.${env.BUILD_NUMBER}"      // Concatenate using Groovy string interpolation
 
      DOCKER_REGISTRY_URL = "https://registry.hub.docker.com"
      DOCKERHUB_USERNAME = "fedora800"
      DOCKERHUB_CREDENTIALS = "cred_dockerhub"
      DOCKER_IMAGE_TAG_1 = "${env.APP_VERSION}"
      DOCKER_IMAGE_TAG_2 = "latest"
      DOCKER_CONTAINER_PORT = "8501"
      DOCKER_PUBLISHED_PORT = "80"

    }
    
/*
  parameters {
    // this is supposed to avoid errors like below in /var/log/syslog or jenkins log when using the Generic WebHook Trigger plugin
    // Sep 23 09:30:16 acg-control1 jenkins[455]: 2024-09-23 09:30:16.778+0000 [id=216]#011WARNING#011hudson.model.ParametersAction#filter: Skipped parameter `jenkins-generic-webhook-trigger-plugin_uuid` as it is undefined on `test-pipeline` (#23). Set `-Dhudson.model.ParametersAction.keepUndefinedParameters=true` to allow undefined parameters to be injected as environment variables or `-Dhudson.model.ParametersAction.safeParameters=[comma-separated list]` to whitelist specific parameter names, even though it represents a security breach or `-Dhudson.model.ParametersAction.keepUndefinedParameters=false` to no longer show this message.
    string(name: 'jenkins-generic-webhook-trigger-plugin_uuid', defaultValue: '', description: 'UUID from the Generic Webhook Trigger plugin')
    // Parameters for the webhook payload (simulate payload if testing)
    string(name: 'param-payload', defaultValue: '', description: 'Webhook payload from GitHub')
  }
*/


  stages {

    stage('Initialization') {
        steps {
            script {
                PrintStageName()  // Print the name of the current stage
            }

            // Step 1: Get and print the Job Time
            script {
                def jobTime = sh(script: "date '+%F %T'", returnStdout: true).trim()
                env.JOB_TIME = jobTime  // Store job time in the environment variable
                echo "Job Time: ${env.JOB_TIME}"
            }

            // Step 2: Clean the Jenkins Workspace
            script {
                cleanWs()  // Clean the Jenkins workspace
                echo "Workspace cleaned successfully."
            }
        }
    }

    stage('Print GitHub Webhook Headers') {
      steps {
        PrintStageName()
          script {
            // NOTE - each of these need to be individually set up on the Jenkins GUI under the "Header parameters" section
            // and the naming convention should be exactly like below example:
            // The "X-GitHub-Delivery" header should be set as Request Header = "x-github-delivery" and leave Value filter blank and here env.x_github_delivery.
            // these are a pain, capitals, hyphen and underscore variable names, so do exactly as done here and in GUI.

            def gitHubDelivery = env.x_github_delivery ?: 'Not available'
            def gitHubEvent = env.x_github_event ?: 'Not available'
            def githubHookId = env.x_github_hook_id ?: 'Not available'
            def gitHubInstallationTargetID = env.x_github_hook_installation_target_id ?: 'Not available'
            def gitHubInstallationTargetType = env.x_github_hook_installation_target_type ?: 'Not available'

            echo "X-GitHub-Delivery : ${gitHubDelivery}"
            echo "X-GitHub-Event : ${gitHubEvent}"
            echo "X-GitHub-Hook-ID : ${githubHookId}"
            echo "X-GitHub-Hook-Installation-Target-ID : ${gitHubInstallationTargetID}"
            echo "X-GitHub-Hook-Installation-Target-Type : ${gitHubInstallationTargetType}"

            //def headers = env.GENERIC_WEBHOOK_TRIGGER_HEADERS ?: 'No Headers Found'
            //echo "Webhook Headers: ${headers}"

            // env shows some interesting variables, need to check out later
            echo "-----------env print --- start ----"
            //sh 'env | sort'                           // too many rows, so for now just show top and bottom of it
            sh 'env > /tmp/env.txt'
            echo "shortened env list :"
            sh '(head -n 5; echo "..."; tail -n 5) < /tmp/env.txt'

            // NOTE: here i can see all the payload data nicely put into individual env variables with prefix of webhook_payload_
            // eg webhook_payload_ref=refs/heads/main
            //    webhook_payload_repository_git_url=git://github.com/fedora800/stocksanalyzer-system.git
            // and of course the whole json in webhook_payload which i am printing in the captureRawPayload_method_2 function
            echo "-----------env print --- end ----"
            // Store some values for use in the next section
            env.GITHUB_HOOK_TARGETID = gitHubInstallationTargetID

          }
      }
    }

    stage('Process Payload Received on the GitHub Webhook') {
            // NOTE - just the Payload, the HEADERS need to be processed differently
            steps {
                PrintStageName()
                script {
//def payload = env.GENERIC_WEBHOOK_TRIGGER_REQUEST_BODY ?: 'No Payload Found'
//echo "Webhook Payload: ${payload}"

                    try {
                        echo "-- Calling captureRawPayload_method_1()  --"
                        captureRawPayload_method_1()
                        echo "-- Calling captureRawPayload_method_2()  --"
                        // A variable called webhook_payload is configured on Jenkins under "Post content parameters"  with Expression = $ and JSONPATH option.
                        captureRawPayload_method_2()
                        echo "-- Calling extractWebhookInfo()  --"
                        extractWebhookInfo()
                        echo "-- Calling createBuildIdentifier()  --"
                        createBuildIdentifier()
                    } catch (Exception e) {
                        echo "Error processing webhook: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
    }


    stage('Pull Code from git PUBLIC repo')  {
      steps {
        PrintStageName()
        script {
          try {
            // Pull code from a GitHub repository
            //git branch: 'main', url: 'https://github.com/fedora800/scratch_project.git'
            git branch: APP_GIT_REPO_BRANCH, credentialsId: APP_GIT_CREDENTIALS_ID, url: APP_GIT_REPO_URL
          }
          catch (err) {
            echo err
          }
        }
      }
    }


/*  -- NOT WORKING -- unable to proceed once it receives the githook, some sort of access problem ----
    stage('Checkout Code from git PRIVATE repo on github.com')  {
      steps {
        PrintStageName()
        script {
          try {
            // Use Jenkins credentials to access the repository
            withCredentials([usernamePassword(credentialsId: "cred-github-fedora800-PAT", passwordVariable: 'VAR_PAT', usernameVariable: 'VAR_USER')]) {
              echo "VAR_USER: ${env.VAR_USER}"
              echo "VAR_PAT: ${env.VAR_PAT}"
              //below is not going to work as this variable is the complete URL itself, so will need to change the variable if we want to use it
              //git branch: env.APP_GIT_REPO_BRANCH, url: "https://${VAR_USER}:${VAR_PAT}@${env.APP_GIT_REPO_URL}"
              git( branch: 'main', credentialsId: "cred-github-fedora800-PAT", url: "https://${VAR_USER}:${VAR_PAT}@github.com/fedora800/stocksanalyzer-system.git")
            }
          }  catch (Exception e) {
            echo "An error occurred: ${e.message}"
            // Fail the stage and stop the pipeline
            error("Stopping pipeline due to error in this stage.")
          }
        }
      }
    }
*/

    stage('Build Python Code - Frontend') {
      steps {
        PrintStageName()
        sh '''
        cd src/frontend
        pip install -r requirements.txt
        '''
        echo "Application Version: ${env.APP_VERSION}"
      }
    }


  stage("Build Docker Image with version passed as argument- Using Shell commands") { 
    steps {
      PrintStageName()
      script {
//            sh echo -e "e[33m THIS IS NOT WORKING, SKIPPING FOR NOW ....e[0m"
        sh """
           sudo docker build -f src/frontend/Dockerfile  --build-arg APP_VERSION=${env.APP_VERSION} \
           --tag ${env.DOCKERHUB_USERNAME}/${env.APP_NAME}:${DOCKER_IMAGE_TAG_1} --tag ${DOCKERHUB_USERNAME}/${env.APP_NAME}:${DOCKER_IMAGE_TAG_2} src/frontend
        """
      }
    }
  }



  stage('Docker Login using Jenkins Credentials ID') {
      steps {
        PrintStageName()
        script {
          // Fetch the username and password token from credentials id and assign values to local variables
          withCredentials([usernamePassword(credentialsId: 'cred_dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_TOKEN')]) {
            // Securely perform Docker login using local environment variables
            // triple single (''') quotes for sh step to ensure that multi-line commands and variable expansions are handled properly by the shell.
            sh '''
            echo "$DOCKER_TOKEN" | sudo docker login -u "$DOCKER_USERNAME" --password-stdin
            '''
          }
        }
        script {
          sh '''
          echo "Builds that are available to push for this app:"
          sudo docker image ls | egrep "REPO|${APP_NAME}"
          '''
        }
      }
  }


  stage("Push Docker Image - Using Shell commands") {
    steps {
      PrintStageName()
      script {
        sh "sudo docker push ${DOCKERHUB_USERNAME}/${APP_NAME}:${DOCKER_IMAGE_TAG_1}"
        sh "sudo docker push ${DOCKERHUB_USERNAME}/${APP_NAME}:${DOCKER_IMAGE_TAG_2}"
      }
    }
  }


  stage('Clone GitOps Repo and push manifest file changes to this GitOps Repo') {
    steps {
      PrintStageName()
      script {
        try {
        // Clone the GitOps repository
          echo 'Cloning the GitOps repository...'
          dir(env.APP_GITOPS_REPO_NAME) {
            withCredentials([usernamePassword(credentialsId: env.APP_GITOPS_CREDENTIALS_ID, usernameVariable: 'VAR_USER', passwordVariable: 'VAR_PAT')]) {
            // Use Jenkins git step to clone the repository securely
            // use the Git URL without credentials. they are still passed securely using the credentialsId parameter. 
            // Jenkins will handle authentication securely using its internal mechanisms (GIT_ASKPASS). 
            // This avoids insecure Groovy string interpolation while still providing the necessary credentials.
              echo "User extracted from Jenkins credentials ${env.APP_GITOPS_CREDENTIALS_ID} : ${env.VAR_USER}"
              echo "PAT (personal access token) extracted from Jenkins credentials ${env.APP_GITOPS_CREDENTIALS_ID} : ${env.VAR_PAT}"
              //git(branch: 'main', credentialsId: env.APP_GITOPS_CREDENTIALS, url: "https://${VAR_USER}:${VAR_PAT}@github.com/fedora800/stocksanalyzer-system.git")
              git(branch: env.APP_GITOPS_BRANCH, credentialsId: env.APP_GITOPS_CREDENTIALS_ID, url: "https://github.com/fedora800/${env.APP_GITOPS_REPO_NAME}.git")
 
              print 'username=' + VAR_USER 
              print 'password=' + VAR_PAT
              print 'username.collect { it } = ' + VAR_USER.collect { it }      // will print username.collect { it } = [f, e, d, o, r, a, 8, 0, 0]
              print 'password.collect { it } = ' + VAR_PAT.collect { it }

              def truncatedPAT = env.VAR_PAT.take(4)  // Take first 4 characters

              // Update requisite YAML files 
              echo '-------------------Updating YAML files... ---------------------------'
              sh """
              echo "User extracted from Jenkins credentials ${env.APP_GITOPS_CREDENTIALS_ID} : ${env.VAR_USER}"
              echo "PAT (personal access token) extracted from Jenkins credentials ${env.APP_GITOPS_CREDENTIALS_ID} : ${env.VAR_PAT}"
              echo "truncatedPAT : ${env.truncatedPAT}"
              pwd
              ls -lR
              #cd kubernetes-manifests/frontend
              echo "Before image change :"
              grep "image: " ${env.DEPLOYMENT_YAML_FILE}
              grep "pl-version: " ${env.DEPLOYMENT_YAML_FILE}
              grep "pl-version: " ${env.SERVICE_YAML_FILE}
              echo "Now updating requisite manifest files ..."
              sed -i "s#pl-version: .*#pl-version: ${env.APP_VERSION}#g" ${env.DEPLOYMENT_YAML_FILE}
              sed -i "s#image: .*#image: ${env.GIT_USER_NAME}/${env.APP_NAME}:${env.APP_VERSION}#g" ${env.DEPLOYMENT_YAML_FILE}
              sed -i "s#pl-version: .*#pl-version: ${env.APP_VERSION}#g" ${env.SERVICE_YAML_FILE}
              echo "After image change :"
              grep "image: " ${env.DEPLOYMENT_YAML_FILE}
              grep "pl-version: " ${env.DEPLOYMENT_YAML_FILE}
              grep "pl-version: " ${env.SERVICE_YAML_FILE}
              """
    
              // Commit and push the changes back to the GitOps repo
              echo 'Committing and pushing changes to GitOps repository...'
              sh """
              git config user.name "Jenkins"
              git config user.email "jenkins@example.com"
              git add ${env.DEPLOYMENT_YAML_FILE} ${env.SERVICE_YAML_FILE}
              git commit -m "Jenkins CI - ${env.JOB_NAME} - Updated kubernetes manifest files for ${env.APP_NAME} with version ${env.APP_VERSION}"
              git remote -v
              git push https://${env.VAR_USER}:${env.VAR_PAT}@github.com/${env.GIT_USER_NAME}/${env.APP_GITOPS_REPO_NAME}.git ${env.APP_GITOPS_BRANCH}
              git log --pretty=format:'%h %ad %s    %D' --date=local -5
              """
            } //with

          } //dir
        }  catch (Exception e) {
          echo "An error occurred: ${e.message}"
          // Fail the stage and stop the pipeline
          error("Stopping pipeline due to error in this stage.")
        } // try
      } // script
    } //steps
  } //stage


  } // end-stages

  post {
      always {
          // Always run steps after the pipeline completes
          echo 'Pipeline finished.'
          //cleanWs() // Clean workspace
      }
      success {
          // Run steps after a successful build
          echo 'Build succeeded!'
      }
      failure {
          // Run steps after a failed build
          echo 'Build failed!'
      }
  } // end-post


} // end-pipeline



//-------------------- section : Functions --------------------

// function to print the stage name more clearly in the jenkins console output, can be called within each stage
def PrintStageName() {
  def currentTime = sh(script: "date +'%T'", returnStdout: true).trim()
  // Print the stage name and current time
  echo "-----------------STAGE: ${env.STAGE_NAME ?: 'Unknown Stage'}-----------------${currentTime}---------"
}

def captureRawPayload_method_1() {

  // When a webhook is received by Jenkins, the Generic Webhook Trigger Plugin intercepts it.
  // The plugin extracts the raw body of the POST request.
  // It then sets this body as the value of the GENERIC_WEBHOOK_TRIGGER_REQUEST_BODY environment variable.
  // This environment variable is then available for use in the Jenkins pipeline script.

  // Capture the raw payload
  def rawPayload = env.GENERIC_WEBHOOK_TRIGGER_REQUEST_BODY ?: '{}'      // **** THIS DOES NOT CAPTURE IT, so not working, sets to {}  ****, but env has it, check there
  // Save the payload to a file in the workspace
  writeFile file: 'webhook_payload-X.json', text: rawPayload
  // Print the file path and contents
  echo "Raw payload saved to: ${env.WORKSPACE}/webhook_payload-X.json"
  sh '''
  ls -l webhook_payload-X.json
  cat webhook_payload-X.json
  '''

}

def captureRawPayload_method_2() {

  // Print the entire payload data that was picked by the Generic Webhook Trigger Plugin 
  // A variable webhook_payload is configured on Jenkins under "Post content parameters"  with Expression = $ and JSONPATH option.
  // echo "webhook_payload = ${env.webhook_payload}"    // WORKS, but prints the huge json, so commented out for now

/*
Post content parameters
Name of variable = webhook_payload
Expression = $
JSONPATH
above expression means we want all the fields from the the payload put into this webhook_payload environment variable.

If we want the Header from the github webhook invocation, eg below - 
X-GitHub-Hook-Installation-Target-Type: repository
Go to "Header parameters" and add Request header = X-GitHub-Hook-Installation-Target-Type and leave Value filter blank
*/

  // Write the JSON content from the env variable to a file
  writeFile file: 'webhook_payload.json', text: "${env.webhook_payload}"

  // Optional: Print the content to verify
  sh '''
  pwd
  ls -l webhook_payload.json
  cat webhook_payload.json | cut -c1-1000
  '''
}


def extractWebhookInfo() {

    // Parse the JSON formatted file into a json type of variable
    def jsonPayload = readJSON text: "${env.webhook_payload}"           // from the env variable
    //def jsonPayload = readJSON file: 'webhook_payload.json'             // from the saved file

    // html_url and git_url fields are typically part of the repository object, not at the root level of the payload
    def htmlUrl       = jsonPayload.repository?.html_url ?: 'Unknown'
    def gitUrl        = jsonPayload.repository?.git_url ?: 'Unknown'
    def repoName      = jsonPayload.repository.full_name ?: 'Unknown'
    def ref           = jsonPayload.ref ?: 'Unknown'
    def branchName    = jsonPayload.ref ? jsonPayload.ref.split('/')[-1] : 'Unknown'
    def commitId      = jsonPayload.after ?: 'Unknown'
    def commitMessage = jsonPayload.head_commit?.message ?: 'Unknown'
    def pusherName    = jsonPayload.pusher?.name ?: 'Unknown'
    echo "Printing main fields received on the GitHub webhook payload for build #${env.BUILD_NUMBER}"
    echo "HTML url: ${htmlUrl}"
    echo "git url: ${gitUrl}"
    echo "Repository: ${repoName}"
    echo "Ref: ${ref}"
    echo "Branch: ${branchName}"
    echo "Commit ID: ${commitId}"
    echo "Commit Message: ${commitMessage}"
    echo "Pushed by: ${pusherName}"
    // Store some values for use in the next section
    env.REPO_NAME = repoName
    env.COMMIT_ID = commitId
    
    // Construct a link between the webhook and the Jenkins build
    def buildLink = "${repoName} commit ${commitId} webhook InstallationTargetID ${GITHUB_HOOK_TARGETID} fired Jenkins Build #${env.BUILD_NUMBER}"
    echo "Link: ${buildLink}"


}


def createBuildIdentifier() {
    def githubDeliveryId = env.HTTP_X_GITHUB_DELIVERY ?: 'Unknown'
    echo "GitHub Delivery ID: ${githubDeliveryId}"
    // Create a unique identifier linking GitHub webhook to Jenkins build
    def linkIdentifier = "${env.BUILD_NUMBER}-${githubDeliveryId}"
    echo "Unique Build Identifier: ${linkIdentifier}"
    // Set this as a build parameter for future reference
    env.GITHUB_JENKINS_LINK = linkIdentifier
    // Additional logging with stored values from previous section
    echo "This build (#${env.BUILD_NUMBER}) is for repository ${env.REPO_NAME}, commit ${env.COMMIT_ID}"
    // Log the Generic Webhook Trigger UUID
    echo "Generic Webhook Trigger UUID: ${params['jenkins-generic-webhook-trigger-plugin_uuid']}"
}

