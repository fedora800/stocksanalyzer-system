
//-------------------- section : Functions --------------------

// function to print the stage name more clearly in the jenkins console output, can be called within each stage
def PrintStageName() {     
  echo "-----------------STAGE: ${env.STAGE_NAME}-----------------"
}

pipeline {

  agent any


// -------------------- section : Environment Variables --------------------

    // Key value pairs which helps passing values to job during job runtime from outside of Jenkinsfile. It’s one way of externalizing configuration. These are GLOBAL USER DEFINED ENVIRONMENT variables.
    // We put it at the top before stages and these env variables will be available at any stage in pipeline. 
    /* Note - 2 other ways
       env variables can also be defined on the jenkins portal via Manage Jenkins > System Configuration > Configure System > Global Properties > Environment Variables
       Initialize Environment variables using sh scripts in Jenkinsfile
    */  
  environment {

    DOCKER_REGISTRY_URL = "https://registry.hub.docker.com"
    DOCKERHUB_CREDENTIALS = "j_dockerhub_credentials"
    // Do not use below in production situations. Use Credentials on Jenkins to store this securely. Refer withCredentials() calls below
    //DOCKERHUB_USERNAME = "fedora800"
    //DOCKERHUB_PASSWORD_TOKEN =      // to not use this unencrpyted, we might need to use jenkins functions to docker login instead of sh scripts
                                      //github push will also fail
    DOCKER_IMAGE_TAG_1 = "${env.BUILD_NUMBER}"
    DOCKER_IMAGE_TAG_2 = "latest"

    GITHUB_REPO_URL = "https://github.com/fedora800/scratch_project.git"
    GITHUB_REPO_BRANCH = "main"
    GITHUB_CREDENTIALS = "j_github_credentials"

    APP_NAME = "basic-nginx-docker-app"


        SLACK_CHANNEL = "#deployment-notifications"
        SLACK_TEAM_DOMAIN = "MY-SLACK-TEAM"
        SLACK_TOKEN = credentials("slack_token")
        DEPLOY_URL = "https://deployment.example.com/"
        // DOCKER_ID = credentials('J_DOCKER_ID')                 // where J_DOCKER_ID is defined as a credential of type secret text on jenkins gui
        // DOCKER_PASSWORD = credentials('J_DOCKER_PASSWORD')     // where J_DOCKER_PASSWORD is defined as a credential of type secret text on jenkins gui

        COMPOSE_FILE = "docker-compose.yml"
        REGISTRY_AUTH = credentials("docker-registry")
        //DOCKERHUB_CREDENTIALS= credentials('dockerhubcredentials')     

        STACK_PREFIX = "my-project-stack-name"
 
       USER_NAME = "joesmith"
       USER_ID = 115         // will be stored as a string value

       IS_BOOLEAN = false   // will be stored as a string value

       LS_OUTPUT = "${sh(script:'ls -lah', returnStdout: true).trim()}"

  }   

  stages {

        // stage-initialization
        stage('Initialization') { NOT-TESTED
            environment { 
                   JOB_TIME = sh (returnStdout: true, script: "date '+%F %T'").trim()
            }   
            steps {
                PrintStageName()
                sh 'echo $JOB_TIME'
            }   
        }   

      // will help us find all the env variables pre-defined for us to use in jenkinsfile
      stage('List All the Jenkins Environment Variables"){ NOT-TESTED
        steps {
          PrintStageName()
          sh "printenv | sort"
        }
      }

      // here i have printed env variables in 2 diff methods
      stage("Print Environment Variables") { // TESTED-AND-WORKS
        steps{
          PrintStageName()
          echo "BUILD_NUMBER = ${env.BUILD_NUMBER}"
          echo "STAGE_NAME = ${env.STAGE_NAME}"
          echo "JOB_NAME=${env.JOB_NAME}"
          echo "NODE_NAME=${env.NODE_NAME}"
          echo "USER=${env.USER}"
          echo "WORKSPACE=${env.WORKSPACE}"
  
          sh "BUILD_NUMBER=$BUILD_NUMBER"
          sh "JOB_NAME=$JOB_NAME"
  
          sh "printenv | sort"
  
        }
      }

    // stage set or use local environment variables in different sections
    stage("Set Env Variables for this Stage - 1") { NOT-TESTED
      environment {
        USER_PATH = "/home/joe"
      }
      steps {

        PrintStageName()
        script {
          env.FILENAME_1_SCR = "testfile-1.csv"
        }

        // IMP - this block will override all types of env variable, including GLOBAL
        withEnv(["FILENAME_2_WENV=here is some value"]) {
            echo "ANOTHER_ENV_VAR = ${env.ANOTHER_ENV_VAR}"
        }
        echo "GLOBAL ENV VARIABLE          - DEPLOY_URL = ${env.DEPLOY_URL}"
        echo "LOCAL ENV VARIABLE           - USER_PATH = ${env.USER_PATH}"
        echo "LOCAL ENV (SCRIPT) VARIABLE  - FILENAME_1_SCR = ${env.FILENAME_1_SCR}"
        echo "LOCAL ENV (WITHENV) VARIABLE - FILENAME_2_SCR = ${env.FILENAME_2_SCR}"
      }
    }


    stage("Clean Jenkins Workspace") { // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          cleanWs()
        }
      }
    }


    stage('Docker Login using Jenkins Credentials ID') {
        steps {
          PrintStageName()
            script {
                // Fetch the username and password token from credentials id and assign values to local variables
                withCredentials([usernamePassword(credentialsId: 'cred_dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_TOKEN')]) {
                    sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_TOKEN'
                }
            }
        }
    }



    stage("Docker Build"){
        steps{
            script{
               withDockerRegistry(credentialsId: 'cred_dockerhub', toolName: 'docker'){   
                   sh "docker build -t amazon-clone ."
                   sh "docker tag amazon-clone deepsharma/amazon-clone:latest "
                }
            }
        }
    }


    stage("Docker Push"){
        steps{
            script{
               withDockerRegistry(credentialsId: 'cred_dockerhub', toolName: 'docker'){   
                   sh "docker push deepsharma/amazon-clone:latest "
                }
            }
        }
    }


  } // end-stages

} // end-pipeline

