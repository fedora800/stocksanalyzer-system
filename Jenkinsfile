//-------------------- section : Functions --------------------

// function to print the stage name more clearly in the jenkins console output, can be called within each stage
def PrintStageName() {
  def currentTime = sh(script: "date +'%T'", returnStdout: true).trim()
  // Print the stage name and current time
  echo "-----------------STAGE: ${env.STAGE_NAME ?: 'Unknown Stage'}-----------------${currentTime}---------"
}


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


    stage('Check Webhook Parameters') {
      steps {
        PrintStageName()
          script {
            echo "Received secret: ${params.cred_jenkins_token_for_github ?: 'Secret not provided'}"
          }
      }
    }



    stage('Print Webhook Payload') {
      steps {
        PrintStageName()
        script {
          echo "Webhook Payload Received:"
            // Print all environment variables
            sh 'env'
            // If you want to print parameters as well, use this:
            echo "Webhook Parameters:"
            echo "${params}"
        }
      }
    }




    // Only proceed if the github webhook received by Jenkins was for my repository
    stage('Check Git Webhook Repository name') {
      steps {
        PrintStageName()
        script {
          def repoName = env.GIT_URL.tokenize('/').last().replace('.git', '')
          echo "env.GIT_URL = ${env.GIT_URL}"
          echo "repoName = ${repoName}"
          if (repoName != 'stocksanalyzer-system') {
            error("This build is only for 'stocksanalyzer-system'. Current repository: ${repoName}")
          }
        }
      }
    }

/*
    stage('Verify Webhook Secret') {
      steps {
        PrintStageName()
        script {
          // Assume the secret from GitHub is available as a parameter in the webhook payload 
          def receivedSecret = params.cred_jenkins_token_for_github
          // Compare payload receieved secret against our defined secret
          if (receivedSecret == WEBHOOK_SECRET_FOR_GITHUB)  {
            echo "Secret verified, proceeding with the pipeline"
          } else {
            error "Webhook secret verification failed"
          }
        }
      }
    }
*/

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



