pipeline {
  agent {
    node {
      label 'builder_cfnnag'
    }
  }
  environment {
    AWS_CREDENTIALS = credentials('aws-php-infra')
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
		sh "aws cloudformation describe-stacks  --stack-name PHP-AWS-Infra  --query \"Stacks[0].Outputs[?OutputKey=='PublicIp'].OutputValue\" --output text  --region eu-central-1" 
        }
      }
    }
}
