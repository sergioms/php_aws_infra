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
			withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'ssh_aws_php_instance', \
                                             keyFileVariable: 'SSH_KEY_SERVER')]){
				sh '''
				export PUBLIC_IP=`aws cloudformation describe-stacks  --stack-name PHP-AWS-Infra  --query "Stacks[0].Outputs[?OutputKey=='PublicIp'].OutputValue" --output text  --region eu-central-1`
				echo aa${PUBLIC_IP}aa
				scp -i aa${SSH_KEY_SERVER}aa src/* ubuntu@${PUBLIC_IP}:/var/www/html
				echo ${SSH_KEY_SERVER} > ./pk.pem
				ls -al 
				cat ./pk.pem
				scp -i ./pk.pem src/* ubuntu@$PUBLIC_IP:/var/www/html
				'''
			}
      }
    }
  }
}
