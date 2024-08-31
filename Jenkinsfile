
/*
-------------------- section : Sample Git Repo structure  --------------------
-------------------- section : Functions --------------------
-------------------- section : Environment Variables --------------------
-------------------- section : Parameters --------------------
-------------------- section : Git Related --------------------
-------------------- section : Build Related --------------------
-------------------- section : Code Quality Related --------------------
-------------------- section : Vulnerability Scan Related --------------------
-------------------- section : Testing Related --------------------
-------------------- section : Metric Checks Related --------------------
-------------------- section : Packaging Related --------------------
-------------------- section : Docker Related (Using Shell commands) --------------------
-------------------- section : Docker Related (Using Jenkins functions) --------------------

*/


//-------------------- section : Sample Git Repo structure  --------------------
my-project/
│
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   └── App.java
│
├── Jenkinsfile  // Main Jenkinsfile
├── Jenkinsfile.test  // Jenkinsfile for test pipelines
├── Jenkinsfile.deploy  // Jenkinsfile for deployment pipelines
└── pom.xml


//-------------------- section : Functions --------------------

// function to print the stage name more clearly in the jenkins console output, can be called within each stage
def PrintStageName() {     TESTED-AND-WORKS
  echo "-----------------STAGE: ${env.STAGE_NAME}-----------------"
}

pipeline {

    //agent any
    //agent none           //if we want to specify different agents for different stages, we can set none here and then the agent under the stage

    agent {
        label 'linux-agents'
    }   

    // below needs to be configured first
    tools {
        maven 'jenkins-maven-3.8.6'
        jdk   'jenkins-jdk-11'
    }   

  triggers {  //before the stages, so no need to configure it seperately in diff section on jenkins gui
    pollSCM 'H/10 * * * *'
  }

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


//-------------------- section : Parameters --------------------

    // different types of parameters that can be set 
    // The parameters directive provides a way for Jenkins job to interact with Jenkins CI/CD users during the running of the build job.
    // we will see 'Build with Parameters' on the Jenkins GUI page
    // i had to manually click to start the build after which it will PAUSE for us to INPUT values in the below prompts on the web page before we proceed.
    parameters {
      // below will show as a 1 line input box, if not put anything, it will take the defined default value
      string(name: 'GREETING', defaultValue: 'Hello', description: 'How should I greet the world?')
      // below will show as a 1 line input box, if not put anything, it will take as null
      string(name: 'NAME', description: 'Please tell me your name?')
      // below will show as large multiline input box, if not put anything, it will take as null
      text(name: 'DESC', description: 'Describe about the job details')
      // below will show a check box with the label and desc given, will take false if not checked
      booleanParam(name: 'SKIP_TEST', description: 'Want to skip running Test cases?')
      // below will show a dropdown box, will take the 1st choice by default if nothing selected
      choice(name: 'BRANCH', choices: ['Master', 'Dev'], description: 'Choose branch')
      // below will show a 1 line input box, will show as concealed and we can change it
      password(name: 'SONAR_SERVER_PWD', description: 'Enter SONAR password')
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

        stage("Stage using Global Boolean Environment Variable") { NOT-TESTED
            steps {
                script {
                    if (env.IS_BOOLEAN) {
                        echo "You can see this message, because \"false\" String evaluates to Boolean.TRUE value"
                    }

                    // we need to call this method to use the boolean expression and value correctly
                    if (env.IS_BOOLEAN.toBoolean() == false) {
                        echo "You can see this message, because \"false\".toBoolean() returns Boolean.FALSE value"
                    }
                }
            }
        }

        // stage-print-params
        stage('Printing Parameters') { NOT-TESTED
            steps {
                echo "Greeting : ${params.GREETING} World!"
                echo "Hi ${params.NAME}"
                echo "Job Details: ${params.DESC}"
                echo "Skip Running Test case ?: ${params.SKIP_TEST}"
                echo "Branch Choice: ${params.BRANCH}"
                echo "SONAR Password: ${params.SONAR_SERVER_PWD}"
            }
        }


        stage('Print the output of ls command stored in Env Variable') { NOT-TESTED
            steps {
                echo "LS_OUTPUT = ${env.LS_OUTPUT}"
            }

        // stage-groovy-logic
        stage('Stage with Groovy code logic') { NOT-TESTED
            steps {
                script {
                    def name = "${params.NAME}"
                    def branch = "${params.BRANCH}"
                    if(branch == "Master") {
                        echo "hello $name, branch is $branch"
                    } else {
                        echo "hello $name, branch is (not master) $branch"
                    }
                }
            }
        }

    // stage-boolean-logic-expression
    stage("Stage with block to execute based on Boolean Condition on Env Variable") { NOT-TESTED
      when {
        expression {
          env.BUILD_SUCCESSFUL.toBoolean() = true
        }
      }
      steps {
        echo "Executing this block now that ${env.BUILD_SUCCESSFUL} is true ..."
      }
    }

        // stage-prepare
        stage("Prepare") { NOT-TESTED
            steps {
                bitbucketStatusNotify buildState: "INPROGRESS"
            }
        }


// -------------------- section : Git Related --------------------

    stage('Pull Code from git PUBLIC repo')  { 		// TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          try {
            // Pull code from a GitHub repository
            //git branch: 'main', url: 'https://github.com/fedora800/scratch_project.git'
            git branch: GITHUB_REPO_BRANCH, credentialsId: GITHUB_CREDENTIALS, url: GITHUB_REPO_URL
          }
          catch (err) {
            echo err
          }
        }
      }
    }


    stage('Pull Code from Private git repo -- method 2')  {		//TESTED-AND-WORKS
      steps {
        PrintStageName()
        git([url: GITHUB_REPO_URL, branch: GITHUB_REPO_BRANCH, credentialsId: GITHUB_CREDENTIALS])
     }
   }


//    this is not required as we have defined a Declarative checkout by enabling Poll-SCM build trigger and configuring the Pipeline script from SCM on Jenkins GUI
//    stage('Stage-Get-git-Repo -- using withCredentials function')  {		//TESTED-AND-WORKS
//      steps {
//        PrintStageName()
//        withCredentials([gitUsernamePassword(credentialsId: 'j_github_credentials', gitToolName: 'git-tool')]) {
//          sh "git fetch --all"
//        }
//      }
//    }



        // stage-git-repo-and-downloads
        stage('git repo connect and download files') {  NOT-TESTED
            //agent linux-agents   // if we want this specific stage to run on this labelled hosts
            steps {
                PrintStageName()
                script {
                         // Get some code from a GitHub repository
                         try{
                           // Get some code from a GitHub repository
                           #git 'https://github.com/LambdaTest/nightwatch-selenium-sample.git'
                           git url: 'https://github.com/naiveskill/devops.git', branch: 'main' 
                           //Download Tunnel Binary
                           sh "wget https://s3.amazonaws.com/lambda-tunnel/LT_Linux.zip"
                      
                           //Required if unzip is not installed
                           sh 'sudo apt-get install --no-act unzip'
                           sh 'unzip -o LT_Linux.zip'
                      
                         }
                         catch (err){
                           echo err
                         }
                }
             }
        }

        // stage-scm-checkout
        stage("SCM Checkout") { NOT-TESTED
        steps { echo "SCM Checkout"  }
        }

        // stage-build
        stage("Build and start test image") { NOT-TESTED
            steps {
                sh "docker-composer build"
                sh "docker-compose up -d"
            }
        }


// -------------------- section : Build Related --------------------
        // stage-build-gradle
        stage('Build using gradlew') {
          steps {
            echo 'Running build automation'
            sh './gradlew build --no-daemon'
            archiveArtifacts artifacts: 'dist/trainSchedule.zip'
          }
        }

      // Python code build
      stage('List All the Jenkins Environment Variables"){ NOT-TESTED
        steps {
          PrintStageName()
          sh '''
          cd myapp
          pip install -r requirements.txt
          '''
        }
      }

// -------------------- section : Code Quality Related --------------------
        // stage-code-review
        stage("Code Review") { NOT-TESTED
        steps { echo "Code Review"  }
        }

        stage("Sonarqube Analysis "){
            steps{
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Netflix \
                    -Dsonar.projectKey=Netflix '''
                }
            }    
        }
        stage("quality gate"){
           steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token' 
                }
            } 
        }

// -------------------- section : Testing Related --------------------

        // stage-test
        /* can comprise of many different testing stages
           or even as many steps of a single test stage
        */
        stage("Unit Test") { NOT-TESTED
        steps { echo "Unit Test"  }
        }

        // stage-integration-test-1
        stage("Integration Test 1") { NOT-TESTED
        steps { echo "Integration Test 1"  }
        }

        // stage-smoke-test
        stage("Smoke Test") { NOT-TESTED
        steps { echo "Smoke Test"  }
        }

        // stage-end-to-end-test
        stage("End to End Test") { NOT-TESTED
        steps { echo "End to End Test"  }
        }

        stage("Run tests") { NOT-TESTED
            steps {
                sh "docker-compose exec -T php-fpm composer --no-ansi --no-interaction tests-ci"
                sh "docker-compose exec -T php-fpm composer --no-ansi --no-interaction behat-ci"
            }

            post {
                always {
                    junit "build/junit/*.xml"
                    step([
                            $class              : "CloverPublisher",
                            cloverReportDir     : "build/coverage",
                            cloverReportFileName: "clover.xml"
                    ])
                }
            }
        }



      // Test Python code example
      stage('Test Python Code"){ NOT-TESTED
        steps {
          PrintStageName()
          sh '''
          cd myapp
          python3 hello.py
          python3 hello.py --name=Brad-Test1
          '''
        }
      }

// -------------------- section : Metric Checks Related --------------------
        // stage-metric-check
        stage("Metrics Check") { NOT-TESTED
        steps { echo "Metrics Check"  }
        }

// -------------------- section : Packaging Related --------------------
        // stage-package
        stage("Package") { NOT-TESTED
        steps { echo "Package"  }
        }

        // stage-deploy
        stage("Deploy") { NOT-TESTED
        steps { echo "Deploy"  }
        }


        stage("Determine new version") { NOT-TESTED
            // Acts like if condition to decide whether to run the particular stage or not
            when {
                branch "master"
            }

            steps {
                script {
                    env.DEPLOY_VERSION = sh(returnStdout: true, script: "docker run --rm -v '${env.WORKSPACE}':/repo:ro softonic/ci-version:0.1.0 --compatible-with package.json").trim()
                    env.DEPLOY_MAJOR_VERSION = sh(returnStdout: true, script: "echo '${env.DEPLOY_VERSION}' | awk -F'[ .]' '{print \$1}'").trim()
                    env.DEPLOY_COMMIT_HASH = sh(returnStdout: true, script: "git rev-parse HEAD | cut -c1-7").trim()
                    env.DEPLOY_BUILD_DATE = sh(returnStdout: true, script: "date -u +'%Y-%m-%dT%H:%M:%SZ'").trim()

                    env.DEPLOY_STACK_NAME = "${env.STACK_PREFIX}-v${env.DEPLOY_MAJOR_VERSION}"
                    env.IS_NEW_VERSION = sh(returnStdout: true, script: "[ '${env.DEPLOY_VERSION}' ] && echo 'YES'").trim()
                }
            }
        }

        stage("Create new version") { NOT-TESTED
            when {
                branch "master"
                environment name: "IS_NEW_VERSION", value: "YES"
            }

            steps {
                script {
                    sshagent(['ci-ssh']) {
                        sh """
                            git config user.email "ci-user@email.com"
                            git config user.name "Jenkins"
                            git tag -a "v${env.DEPLOY_VERSION}" \
                                -m "Generated by: ${env.JENKINS_URL}" \
                                -m "Job: ${env.JOB_NAME}" \
                                -m "Build: ${env.BUILD_NUMBER}" \
                                -m "Env Branch: ${env.BRANCH_NAME}"
                            git push origin "v${env.DEPLOY_VERSION}"
                        """
                    }
                }

                sh "docker login -u=$REGISTRY_AUTH_USR -p=$REGISTRY_AUTH_PSW ${env.REGISTRY_ADDRESS}"
                sh "docker-compose -f ${env.COMPOSE_FILE} build"
                sh "docker-compose -f ${env.COMPOSE_FILE} push"
            }
        }


// -------------------- section : Docker Related (Using Shell commands) --------------------

    stage("Build Docker Image - Using Shell commands") {                // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          sh "docker build --tag $DOCKERHUB_USERNAME/$APP_NAME:$DOCKER_IMAGE_TAG_1 --tag $DOCKERHUB_USERNAME/$APP_NAME:$DOCKER_IMAGE_TAG_2 ."
        }
      }
    }

    stage("Connect to Docker Registry and authenticate with credentials - Using Shell commands") {      // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          sh "hostnamectl"              // just run this shell command to show which jenkins agent/host this is being built on
          //sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
          //sh "sudo docker login -u ${env.DOCKERHUB_USERNAME} -p ${env.DOCKERHUB_PASSWORD_TOKEN}"
          // below is more secure practice
          //sh "echo $DOCKERHUB_PASSWORD_TOKEN | sudo docker login -u $DOCKERHUB_USERNAME --password-stdin"
          // throws below error -
//sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
//sudo: a password is required
          // but this is seen online - https://thetechdarts.com/deploy-to-dockerhub-using-jenkins-declarative-pipeline/ 
          // added jenkins userid to docker group and then did below, which worked
          sh "echo $DOCKERHUB_PASSWORD_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin"
        }
      }
    }


    stage("Push Docker Image - Using Shell commands") {         // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
//        sh "docker push jsmith/spring-petclinic:latest" // example
          sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:$DOCKER_IMAGE_TAG_1"
          sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:$DOCKER_IMAGE_TAG_2"
        }
      }
    }

    stage("Logout from the Docker Registry - Using Shell commands") {           // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          sh "docker logout"
        }
      }
    }


    stage("Clean up local docker images - Using Shell commands") {              // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          sh "docker image rm $DOCKERHUB_USERNAME/$APP_NAME:$DOCKER_IMAGE_TAG_1"
          sh "docker image rm $DOCKERHUB_USERNAME/$APP_NAME:$DOCKER_IMAGE_TAG_2"
        }
      }
    }


// -------------------- section : Docker Related (Using Jenkins functions) --------------------


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

    stage("Connect to Docker Registry and authenticate with credentials - Using Jenkins function") {           // TESTED-AND-WORKS
      steps {
        PrintStageName()
          script {
            // needs Docker Pipeline plugin
            // Connect to Docker Registry
            //docker.withRegistry($DOCKER_REGISTRY_URL, $DOCKERHUB_CREDENTIALS) {
            docker.withRegistry('https://registry.hub.docker.com', 'j_dockerhub_credentials') {
            // Build the image locally
            def myDockerImage1 = docker.build("${DOCKERHUB_USERNAME}/${APP_NAME}:${DOCKER_IMAGE_TAG_1}")
            def myDockerImage2 = docker.build("${DOCKERHUB_USERNAME}/${APP_NAME}:${DOCKER_IMAGE_TAG_2}")
  //          eg. dockerImage = docker.build("monishavasu/my-react-app:latest")
            /* Push the container to the Docker Registry */
            myDockerImage1.push()
            myDockerImage2.push()
          }
        }
      }
    }

   stage("Push to Dockerhub") {      NOT-TESTED
     when { 
       equals 
          expected: "true", 
          actual: "${params.PushImage}" }
     steps {
       script {
         echo "Pushing the image to docker hub"
         def localImage = "${params.Image_Name}:${params.Image_Tag}"
      
         // pcheajra is my username in the DockerHub
         // You can use your username
         def repositoryName = "pchejara/${localImage}"
      
         // Create a tag that going to push into DockerHub
         sh "docker tag ${localImage} ${repositoryName} "
         docker.withRegistry("", "DockerHubCredentials") {
           def image = docker.image("${repositoryName}");
           image.push()
         }
       }
    }
  }
  post {
     always {
        script {
           echo "I am execute always"
        }
     }
     success {
        script {
           echo "I am execute on success"
        }
     }
     failure {
        script {
           echo "I am execute on failure"
        }
     }
  }

// DOCKER stages -- USING JENKINS FUNCTIONS  (end)
// --------------------------------------------------------------------------------

// -------------------- section : Vulnerability Scan Related --------------------

        // stage-trivy-artifact-scan
        stage("Scan the Docker Image with Trivy using static analysis for vulneribilities") { NOT-TESTED
          ## to do
        }

        // stage-docker-build
        stage('Build and Publish Docker Image') { NOT-TESTED
            when {
                branch 'master'  //only run these steps on the master branch
            }
            steps {
                /*
                 * Multiline strings can be used for larger scripts. It is also possible to put scripts in your shared library
                 * and load them with 'libaryResource'
                 */
                sh """
          docker build -t ${IMAGE} .
          docker tag ${IMAGE} ${IMAGE}:${VERSION}
          docker push ${IMAGE}:${VERSION}
        """
            }
            post {
                failure {
                    // notify users when this step fails
                    mail to: 'team@example.com',
                            subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                            body: "Something is wrong with ${env.BUILD_URL}"
                }
            }
        }


        // stage-docker-hub
        stage("Push Newly Built Image to DockerHub") { NOT-TESTED

          steps {
             script {
               sh "sudo docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_CREDENTIALS}"
               sh "sudo docker push XXXX/YYYY"
             }
          }

        }

      stage("Build docker images") {		NOT-TESTED
         steps {
            script {
               echo "Bulding docker images"
               def buildArgs = """\
--build-arg HTTP_PROXY=${params.HTTP_PROXY} \
--build-arg HTTPS_PROXY=${params.HTTPS_PROXY} \
-f Dockerfile \
."""
                docker.build(
                   "${params.Image_Name}:${params.Image_Tag}",
                   buildArgs)
            }
         }
      }
   }

        // stage-prune-images
        stage("Prune Docker Images") { NOT-TESTED

          # this is not exactly prune, but just deleting the specific image 
          steps {
            script {
              sh "sudo docker image rm ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
              sh "sudo docker image rm ${DOCKER_IMAGE_NAME}:latest"
        }



        // stage-apply-docker-changes-to-kubernetes
        stage("Apply Docker Image changes into Kubernetes Deployment File") { NOT-TESTED

          steps {
            script {
              sh """
                 echo "--pre change--"; cat deployment.yml
                 sed -i 's/${APP_NAME}.*/${APP_NAME}:${DOCKER_IMAGE_TAG}/g' deployment.yml
                 echo "--post change--"; cat deployment.yml

                 sudo docker image rm ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                 sudo docker image rm ${DOCKER_IMAGE_NAME}:latest
              """
        }


        // stage-commit-kubernetes-changes
        stage("Push the Kubernetes Changes into git") { NOT-TESTED

          steps {
            script {
              sh """
                 git config --global user.name "fedora800"
                 git config --global user.email "fedora800@gmail.com"
                 git add deployment.yml
                 git commit -m "k8 deployment file updated - by jenkins - ${env.BUILD_NUMBER}"
              """
             withCredentials([gitUsernamePassword(credentialsId: 'jenkins-github-credentials-id', gitToolName: 'git-tool')]) {
               sh "git push https://github.com/fedora800/myproject1.git main"
             }
 
        }

        // stage-push-to-gitops-git-repo-manifest-file      
        stage("Push the changed deployment file to Git") {
            steps {
                sh """
                    git config --global user.name "dmancloud"
                    git config --global user.email "dinesh@dman.cloud"
                    git add deployment.yaml
                    git commit -m "Updated Deployment Manifest"
                """
                withCredentials([gitUsernamePassword(credentialsId: 'github', gitToolName: 'Default')]) {
                    sh "git push https://github.com/dmancloud/gitops-complete-prodcution-e2e-pipeline main"
                }
            }
        }

    // stage-input-basic-manual-approval
    /*
       On GUI, will wait for this stage, when clicked it will show my msg "Are you confirming to deploy change into Production ?" with button options of "Yes" and "Abort"
       if clicked on "Yes" --->
[Pipeline] stage
[Pipeline] { (Manual Approval Before Deploying into Production) (hide)
[Pipeline] input
Are you confirming to deploy change into Production ?
Yes or Abort
Approved by Admin User
[Pipeline] echo
-----------------Manual Approval Before Deploying into Production-----------------
[Pipeline] echo
User has confirmed production deployment ...
[Pipeline] echo
Now deploying to PROD ...
Post stage
[Pipeline] echo
--in post always--
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
       On clicking abort, job status will change to Aborted and console output ---->
Rejected by Admin User
org.jenkinsci.plugins.workflow.actions.ErrorAction$ErrorId: 4c852ee0-24fb-4c9a-986a-d680f42acf41
Finished: ABORTED
    */
    stage("Manual Approval Before Deploying into Production") { // TESTED-AND-WORKS
      input {
        message "Are you confirming to deploy change into Production ?"
        ok "Yes"
        //submitter: list of users or groups who are allowed to submit this input, default is any user.
        //submitter "ssbostan,admin,admins,managers"
        //submitterParameter: if this option is used, can be used to set submitter username in the environment variables.
        //submitterParameter "SUBMITTER_USERNAME"
      }
      steps {
        PrintStageName()
        echo "User has confirmed production deployment ..."
        echo "Now deploying to PROD ..."
      }
      post {
        always {
          echo "--in post always--"
        }
      }
    }

    // stage-input-param-get-choice
    stage("Manual Choice of values using parameters") {       // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          env.MY_CHOICE_ENV = input message: 'User input required',
            parameters: [choice(name: 'Whats your choice ? ', choices: 'no\nyes', description: 'Choose "yes" if you want to deploy this build')]
        }
      }
    }


    // if we had chosen "yes", it will print "You had selected (yes) - yes ..."
    // if we had chosen "no", it will completely skip this stage due to the when conditional
    stage('Inform about the choice Variable') {            // TESTED-AND-WORKS
      when {
        environment name: 'MY_CHOICE_ENV', value: 'yes'
      }
      steps {
        PrintStageName()
        echo "You had selected (yes) - ${env.MY_CHOICE_ENV} ..."
      }
    }


    // stage-input-request-username-password
    stage ("Request UserName and Password") {    // TESTED-AND-WORKS
      steps {
        PrintStageName()
        script {
          env.USERNAME = input message: 'Please enter the username',
            parameters: [string(defaultValue: '', description: 'Username for the app', name: 'Username')]
          env.PASSWORD = input message: 'Please enter the password',
            parameters: [password(defaultValue: '', description: 'Passwd for the app', name: 'Password')]
        }
        echo "Username: ${env.USERNAME}"
        echo "Password: ${env.PASSWORD}"
      }
    }

    // stage-input-multiple-parameters
    // the stage will wait with a popup showing "Select options: The paused input step uses advanced input options. <href Please redirect to approve >
    // where once clicked on the above href, it will take us to a page which will ask us to put all the inputs
    // the echo will give -> Env: [Options:Foo, textInput:data-textInput-box, submitterBy:admin, Check1:false, credentialsParam:, inputText:data-inputText-row-box, PasswordField:None, textField:data-textField-box]
    stage("Take in as Input Multiple Parameters") {   //TESTED-AND-WORKS
      steps {
        timeout(time: 2, unit: 'HOURS') { //SECONDS | MINUTES | HOURS | DAYS
          script {
            def userInput =
                  input( id: 'input'
                    , message: 'Select options :'
      //            , submitter: 'asanchez' // only this user can submit the form, comment to skip
                    , submitterParameter: 'submitterBy' // return the name of the user submitter
                    , parameters: [
                       //Params
                       booleanParam(name: 'Check1', defaultValue: false)
                       , [$class: 'TextParameterDefinition', defaultValue: 'Dummy Text', description: 'A simple text param', name: 'textInput']
                       , text(defaultValue: 'LOREM', description: '', name: 'textField')
                       , string(defaultValue: 'dummy text', description: '', name: 'inputText', trim: false)
                       , credentials(credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl', defaultValue: '', description: '', name: 'credentialsParam', required: true)
                     , choice(choices: ['Foo', 'Bar', 'Sed'], description: '', name: 'Options')
                     , password(defaultValue: 'None', description: '', name: 'PasswordField')
                       ])

                   echo("Env: " + userInput)

          }
        }
      }
    }




        // stage-manual-approval
        stage("Manual Approval Before Deploying into Production") { NOT-TESTED
          steps {
            script {
              # gives approvers 10mins to approve, else abort this stage & pipeline
              timeout(10) {
                emailext body: "<br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br>Build URL: ${env.BUILD_URL} <br> Please review & approve deployment via the Build URL link", recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'Requesting Approval - ${env.BUILD_NUMBER} - ${env.BUILD_URL}'
                input {
                  message "Are you confirming to deploy change into Production ?"
                  ok "Deploy"
                }
              }
            }
          }

          post {
            always {
            }
          }
        }


        // stage-update-manifest-files-into-a-seperate-gitops-repo
        stage("Change the Kubernetes Manifest files and git push them into the seperate GitOps repo") { NOT-TESTED
        // ArgoCD will be monitoring this gitops repo and will apply this updated deployment.yml to kubernetes cluster automatically
           script {
             catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
               withCredentials([usernamePassword(credentialsId: 'github', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                 //def encodedPassword = URLEncoder.encode("$GIT_PASSWORD",'UTF-8')
                 sh "git config user.email raj@cloudwithraj.com"
                 sh "git config user.name RajSaha"
                 //sh "git switch master"
                 sh "cat deployment.yaml"
                 sh "sed -i 's+raj80dockerid/test.*+raj80dockerid/test:${DOCKERTAG}+g' deployment.yaml"
                 sh "cat deployment.yaml"
                 sh "git add ."
                 sh "git commit -m 'Done by Jenkins Job changemanifest: ${env.BUILD_NUMBER}'"
                 sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/${GIT_USERNAME}/kubernetesmanifest.git HEAD:main"
               }
             }
           }
        }

        // stage-deploy-into-kubernetes
        stage("Deploy to Kubernetes Cluster") { NOT-TESTED
          sh "kubectl apply -f deployment.yml"
        }

        // stage-canary-deploy
        stage('CanaryDeploy') {
          when {
            branch 'master'
          }
          environment {
            CANARY_REPLICAS = 1
          }
          steps {
            kubernetesDeploy(
              kubeconfigId: 'kubeconfig',
              configs: 'train-schedule-kube-canary.yml',
              enableConfigSubstitution: true
            )
          }
        }
      
        //stage-deploy-to-prod-kubernetes-cluster
        stage('Deploy To Production Kubernetes cluster') {
            when {
                branch 'master'
            }
            environment {
                CANARY_REPLICAS = 0
            }
            steps {
                input 'Deploy to Production?'
                milestone(1)
                kubernetesDeploy(
                    kubeconfigId: 'kubeconfig',
                    configs: 'train-schedule-kube-canary.yml',
                    enableConfigSubstitution: true
                )
                kubernetesDeploy(
                    kubeconfigId: 'kubeconfig',
                    configs: 'train-schedule-kube.yml',
                    enableConfigSubstitution: true
                )
            }
        }

        // stage-deploy-prod
        stage("Deploy to production") { NOT-TESTED
            agent { node { label "swarm-prod" } }

            when {
                branch "master"
                environment name: "IS_NEW_VERSION", value: "YES"
            }

            steps {
                sh "docker login -u=$REGISTRY_AUTH_USR -p=$REGISTRY_AUTH_PSW ${env.REGISTRY_ADDRESS}"
                sh "docker stack deploy ${env.DEPLOY_STACK_NAME} -c ${env.COMPOSE_FILE} --with-registry-auth"
            }

            post {
                success {
                    slackSend(
                            teamDomain: "${env.SLACK_TEAM_DOMAIN}",
                            token: "${env.SLACK_TOKEN}",
                            channel: "${env.SLACK_CHANNEL}",
                            color: "good",
                            message: "${env.STACK_PREFIX} production deploy: *${env.DEPLOY_VERSION}*. <${env.DEPLOY_URL}|Access service> - <${env.BUILD_URL}|Check build>"
                    )
                }

                failure {
                    slackSend(
                            teamDomain: "${env.SLACK_TEAM_DOMAIN}",
                            token: "${env.SLACK_TOKEN}",
                            channel: "${env.SLACK_CHANNEL}",
                            color: "danger",
                            message: "${env.STACK_PREFIX} production deploy failed: *${env.DEPLOY_VERSION}*. <${env.BUILD_URL}|Check build>"
                    )
                }
            }
        }


        stage("Trigger CD Pipeline") {
            steps {
                script {
                    sh "curl -v -k --user admin:${JENKINS_API_TOKEN} -X POST -H 'cache-control: no-cache' -H 'content-type: application/x-www-form-urlencoded' --data 'IMAGE_TAG=${IMAGE_TAG}' 'https://jenkins.dev.dman.cloud/job/gitops-complete-pipeline/buildWithParameters?token=gitops-token'"
                }
            }

        }


        // stage-verify-deployment
        stage("Verify App Deployment") { NOT-TESTED
          ## to do
        }


        // stage-monitor
        stage("Monitor") { NOT-TESTED
            steps { echo "Monitor"  }
        }

    } // end-stages

    // do below post all the stages
    post {
        always {
            sh "docker-compose down || true"
        }

        success {
            bitbucketStatusNotify buildState: "SUCCESSFUL"
        }

        failure {
          // notify users when the Pipeline fails
          mail to: 'team@example.com',
          subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
          body: "Something is wrong with ${env.BUILD_URL}"
    }
    }

    //another post block example for reference
    post {
        failure {
            emailext body: '''${SCRIPT, template="groovy-html.template"}''', 
                    subject: "${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} - Failed", 
                    mimeType: 'text/html',to: "dmistry@yourhostdirect.com"
            }
         success {
               emailext body: '''${SCRIPT, template="groovy-html.template"}''', 
                    subject: "${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} - Successful", 
                    mimeType: 'text/html',to: "dmistry@yourhostdirect.com"
          }      
    }



}

// $ grep -n "section|stage\(" Jenkinsfile.reference     # run this to get all the stages




--------------------------------------------------------------------------------
// others i have gathered from online articles


// -------------------- section : Vulnerability Scan Related --------------------

        stage('Install Dependencies') {
            steps {
                sh "npm install"
            }
        }

        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage('TRIVY FS SCAN') {
            steps {
                sh "trivy fs . > trivyfs.txt"
            }
        }

        stage("TRIVY"){
            steps{
                sh "trivy image deepsharma/amazon-clone:latest > trivyimage.txt" 
            }
        }

        stage("Docker Build & Push"){
            steps{
                script{
                   withDockerRegistry(credentialsId: 'docker', toolName: 'docker'){   
                       sh "docker build -t amazon-clone ."
                       sh "docker tag amazon-clone deepsharma/amazon-clone:latest "
                       sh "docker push deepsharma/amazon-clone:latest "
                    }
                }
            }
        }


        stage("TRIVY"){
            steps{
                sh "trivy image brodevops/netflix:latest > trivyimage.txt" 
            }
        }


        stage('Deploy to container'){
            steps{
                sh 'docker run -d --name amazon-clone -p 3000:3000 deepsharma/amazon-clone:latest'
            }
        }






--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
