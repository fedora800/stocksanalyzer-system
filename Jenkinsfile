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
    APP_GIT_REPO_URL = "https://github.com/fedora800/stocksanalyzer-system.git"
    APP_GIT_REPO_BRANCH = "main"
    APP_GIT_REPO_CREDENTIALS_ID = "cred-github-fedora800-PAT"

    APP_GITOPS_REPO_URL = 'https://github.com/your-username/gitops-stocksanalyzer-system.git' 
    APP_GITOPS_BRANCH = 'main'
    APP_GITOPS_CREDENTIALS_ID = 'cred-github-fedora800-PAT'



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


    stage('Pull Code from git PUBLIC repo')  {
      steps {
        PrintStageName()
        script {
          try {
            // Pull code from a GitHub repository
            //git branch: 'main', url: 'https://github.com/fedora800/scratch_project.git'
            git branch: APP_GIT_REPO_BRANCH, credentialsId: APP_GIT_REPO_CREDENTIALS_ID, url: APP_GIT_REPO_URL
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


  stage('Run Docker Container') {
          steps {
              script {
                  PrintStageName()
                  try {
                      // Stop and remove any existing container with the same name
                      sh """
                          if [ \$(sudo docker container ls -a -f name=${env.APP_NAME} -q) ]; then
                              sudo docker stop ${env.APP_NAME}
                              sudo docker rm -f ${env.APP_NAME}
                          fi
                      """

//                        // Run the Docker container
//                        sh """
//                           sudo docker run -d --name ${env.APP_NAME} \
//                           --publish ${DOCKER_PUBLISHED_PORT}:${DOCKER_CONTAINER_PORT} ${DOCKERHUB_USERNAME}/${APP_NAME}:${DOCKER_IMAGE_TAG_2} \
//                           ${env.APP_NAME} 
//                        """
//                        // sudo docker run -d --name stocksanalyzer-frontend-app --publish 80:8501 fedora800/stocksanalyzer-frontend-app:latest stocksanalyzer-frontend-app
                  } catch (Exception e) {
                      echo "Failed to run Docker container: ${e}"
                      currentBuild.result = 'FAILURE'
                  }
              }
          }
    }



    stage('Clone GitOps Repo and push manifest file changes to this GitOps Repo') {  // NOT-TESTED
      steps {
        script {
          PrintStageName()
          // Clone the GitOps repository
          echo 'Cloning the GitOps repository...'
          withCredentials([usernamePassword(credentialsId: "cred-github-fedora800-PAT", passwordVariable: 'VAR_PAT', usernameVariable: 'VAR_USER')]) {
          // use the Git URL without credentials. they are still passed securely using the credentialsId parameter. Jenkins will handle authentication securely using its internal mechanisms (GIT_ASKPASS). This avoids insecure Groovy string interpolation while still providing the necessary credentials.
            git branch: 'main', credentialsId: "cred-github-fedora800-PAT", url: "https://github.com/fedora800/gitops-stocksanalyzer-system.git"
          }

/*
          sh """
          git clone -b ${APP_GITOPS_BRANCH} https://${env.APP_GITOPS_REPO_URL} gitops-repo
          cd gitops-repo
          """
*/
          // Update requisite YAML files 
          // Must use Groovy string interpolation (${}) inside a double-quoted Groovy string (""").
          echo 'Updating YAML files...'
          sh """
          echo "Now updating kubernetes-manifests/frontend/dpl-frontend.yaml"
          cd kubernetes-manifests/frontend
          pwd
          ls -l
          echo "Before image change :"
          grep "image: " dpl-frontend.yaml
          echo "env.BUILD_NUMBER  = ${env.BUILD_NUMBER}"
          sed -i "s#image: .*stocksanalyzer-frontend-app.*#image: fedora800/stocksanalyzer-frontend-app:1.0.${env.BUILD_NUMBER}#g" dpl-frontend.yaml
          echo "After image change :"
          grep "image: " dpl-frontend.yaml
          """
//                    def buildNumber = env.BUILD_NUMBER
//                    sh "sed -i 's#image: .*stocksanalyzer-frontend-app.*#image: fedora800/stocksanalyzer-frontend-app:1.0.${buildNumber}#g' dpl-frontend.yaml"


/*
          // Commit and push the changes back to the GitOps repo
          echo 'Committing and pushing changes to GitOps repository...'
          sh """
          cd gitops-repo
          git config user.name "Jenkins"
          git config user.email "jenkins@example.com"
          git add .
          git commit -m "Update deployment YAML with build ${BUILD_NUMBER}"
          git push https://${env.APP_GITOPS_CREDENTIALS_ID}@${APP_GITOPS_REPO_URL} ${APP_GITOPS_BRANCH}
          """
*/
        }
      }
    }


    stage('Cleaning up old Docker images')  {    // CURRENTLY, its not printing FINAL REMOVE_LIST, though that variable is getting done properly in loop
      steps {
        // Clean up temporary files, containers, etc.
        echo 'Cleaning up...'

        script {
          PrintStageName()  
  
          // This will remove all dangling images (images with no tags)
          sh "sudo docker image prune -f"
  
          // Remove specific images older than a specified number of days
          sh '''
            DAYS_OLD=30

            # Get current date in seconds since epoch
            current_date=$(date +%F)

            REMOVE_LIST=""
            # Convert current date to epoch time format
            current_date_epoch=$(date -d "$current_date" +%s)
            # List images and filter based on creation date
            sudo docker images --format "{{.ID}} {{.Repository}} {{.Tag}} {{.CreatedAt}}" | while read -r id repo tag created_at; do
                # Extract date part from created_at and remove timezone info
                formatted_date=$(echo "$created_at" | awk '{print $1}')
                # Convert creation date to epoch time format
                created_date_epoch=$(date -d "$formatted_date" +%s 2>/dev/null)

                if [ -z "$created_date_epoch" ]; then
                    echo "Date parsing failed for image $repo:$tag"
                    continue
                fi

                # Calculate age in days
                age_days=$(( (current_date_epoch - created_date_epoch) / 86400 ))

                if [ "$age_days" -ge "$DAYS_OLD" ]; then
                  echo "$id - $repo:$tag is $age_days days old and will be deleted"
                  echo "REMOVE_LIST DEBUG1 ====${REMOVE_LIST}==="
                  REMOVE_LIST="${REMOVE_LIST} $id"
                  echo "REMOVE_LIST DEBUG2 ====${REMOVE_LIST}==="
                fi
            done
            echo "Deleting old Docker images..."
            echo "REMOVE_LIST ----------------FINAL------------ ====${REMOVE_LIST}==="
            sudo docker image rm -f $REMOVE_LIST
          '''
        }
      } //steps
    }


  } // end-stages

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
  } // end-post


} // end-pipeline



