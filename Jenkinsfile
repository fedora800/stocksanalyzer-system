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

      DOCKER_REGISTRY_URL = "https://registry.hub.docker.com"
      DOCKERHUB_CREDENTIALS = "cred_dockerhub"
      DOCKER_IMAGE_TAG_1 = "${env.BUILD_NUMBER}"
      DOCKER_IMAGE_TAG_2 = "latest"
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


    stage('Checkout Code from git PUBLIC repo on github.com')  {    // TESTED-AND-WORKS
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
        }
      }


      stage('Test') {
          steps {
              // Run tests (e.g., unit tests, integration tests)
              echo 'Running tests...'
          }
      }

    stage("Build a Docker Image") {     //NOT TESTED
      steps {
        PrintStageName()
          script {
            docker.withRegistry($DOCKER_REGISTRY_URL, $DOCKERHUB_CREDENTIALS) {
            //docker.withRegistry('https://registry.hub.docker.com', 'j_dockerhub_credentials') {
            // Build the image locally
            def myDockerImage1 = docker.build("${env.DOCKERHUB_USERNAME}/${env.APP_NAME}:${env.DOCKER_IMAGE_TAG_1}")
            def myDockerImage2 = docker.build("${env.DOCKERHUB_USERNAME}/${env.APP_NAME}:${env.DOCKER_IMAGE_TAG_2}")
          }
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
                  sh 'echo $DOCKER_TOKEN | docker login -u $DOCKER_USERNAME --password-stdin'
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



