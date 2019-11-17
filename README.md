# php_aws_infra
Setup PHP server in AWS

List of tasks:
* setup basic infra and instance (create basic AWS Cloud Formation template)- OK
* setup httpd and php on instance - OK
* setup Jenkinsfile (CICD pipeline) to deploy workload from github repo using Jenkins - OK
* setup Jenkinsfile (CICD pipeline) to deploy infra from github repo (AWS CloudFormation template) 
* Add LB and WAF, block XSS in WAF, setup up logging
* Setup monitoring for request containing XSS payloads

What should be done in addition:
* TLS support, disable HTTP at all, add HSTS (Strict Transport Security Headers)
* harden Linux server image (build a minimal image, harden apache2 and php config)
* scan image (vulnerability scannning) in the CICD pipeline
* scan code to be deployed (Static Source Code Scans, Open Source Libraries scan)
* run in isolated VPC
