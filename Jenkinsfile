pipeline {
  agent {
    node {
      label 'builder_cfnnag'
    }
  }
  environment {
    AWS_CREDENTIALS = credentials('f6574ca3-ca32-4ca4-85a0-c080714a484f')
    AWS_ACCESS_KEY_ID = "${env.AWS_CREDENTIALS_USR}"
    AWS_SECRET_ACCESS_KEY = "${env.AWS_CREDENTIALS_PSW}"
  }
  stages {
    stage('Initialize') {
      steps {
        sh "aws --version"
        sh "aws iam get-user"
        sh "echo \"Jenkins Workspace: ${env.WORKSPACE}\""
        sh "echo \"Jenkins Build ID: ${env.BUILD_ID}\""
      }
    }
    stage('Setup Infra') {
      steps {
        script {
          try {
			sh "/bin/bash echo $AWS_CREDENTIALS"
			sh "/bin/bash echo $AWS_ACCESS_KEY_ID"
			sh "/bin/bash echo $AWS_SECRET_ACCESS_KEY"
			sh "/bin/bash aws cloudformation describe-stacks  --stack-name PHP-AWS-Infra  --query \"Stacks[0].Outputs[?OutputKey=='PublicIp'].OutputValue\" --output text" 

          }
          catch(Exception e) {
            currentBuild.currentResult = "FAILURE"
          }
          finally {
          }
        }
      }
    }
}