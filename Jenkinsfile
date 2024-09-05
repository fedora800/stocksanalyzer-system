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
      GITHUB_REPO_URL = "https://github.com/fedora800/stocksanalyzer-system.git"
      GITHUB_REPO_BRANCH = "main"

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


    stage('Checkout Code from git PUBLIC repo on github.com')  {
      steps {
        PrintStageName()
        script {
          try {
            // Pull code from a GitHub repository
            //example - git branch: 'main', url: 'https://github.com/fedora800/scratch_project.git'
            git branch: GITHUB_REPO_BRANCH, url: GITHUB_REPO_URL
          }
          catch (err) {
            echo err
          }
        }
      }
    }

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


      stage('Test') {
          steps {
              // Run tests (e.g., unit tests, integration tests)
              echo 'Running tests...'
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
            echo "Builds available to push for this app:"
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


    stage('Run Docker Container') {
            steps {
                script {
                    PrintStageName()
                    try {
                        // Stop and remove any existing container with the same name
                        sh """
                            if [ \$(sudo docker ps -q -f name=${env.APP_NAME}) ]; then
                                sudo docker stop ${env.APP_NAME}
                                sudo docker rm ${env.APP_NAME}
                            fi
                        """

                        // Run the Docker container
                        sh """
                           sudo docker run -d --name ${env.APP_NAME} \
                           --publish ${DOCKER_PUBLISHED_PORT}:${DOCKER_CONTAINER_PORT} ${DOCKERHUB_USERNAME}/${APP_NAME}:${DOCKER_IMAGE_TAG_2} \
                           ${env.APP_NAME} 
                        """
                        // sudo docker run -d --name null --publish 80:8501 fedora800/stocksanalyzer-frontend-app:latest stocksanalyzer-frontend-app
                        // 051d2d130a3dc056846d07c7f4962380d225a5a137791c32c7d4978925188019

                    } catch (Exception e) {
                        echo "Failed to run Docker container: ${e}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
      }

      stage('Deploy') {
          steps {
              // Deploy to a target environment (e.g., staging, production)
              echo 'Deploying the application...'
          }
      }

      stage('Cleanup') {
          steps {
              // Clean up temporary files, containers, etc.
              echo 'Cleaning up...'
          }
      }
  }

  post {
      always {
          // Always run steps after the pipeline completes
          echo 'Pipeline finished.'
          cleanWs() // Clean workspace
      }
      success {
          // Run steps after a successful build
          echo 'Build succeeded!'
      }
      failure {
          // Run steps after a failed build
          echo 'Build failed!'
      }

  } // end-stages

} // end-pipeline



