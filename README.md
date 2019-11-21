# php_aws_infra
Setup PHP server in AWS

What should be done in addition:
* TLS support, disable HTTP at all, add HSTS (Strict Transport Security Headers)
* Add Security Headers: Block XSS, CSP, disable Cache 
* Infrastructure Monitoring 
* Security Smoke tests: Nmap, Public buckets, OWASP ZAP for basic tests (http headers, including cache), OWASP ZAP for xss (maybe something else?)
* harden Linux server image (build a minimal image, harden apache2 and php config)
* scan image (vulnerability scannning) in the CICD pipeline
* scan code to be deployed (Static Source Code Scans, Open Source Libraries scan)
* run in isolated VPC
* Ensure merge to master and deployments only happen if code reviewed. Align with branching strategy

## Deliverables

Following deliverables are included:
* **src/xss.php**: simple php application which contains an easy to exploit XSS. Parameter _name_ provided in querystring will be just printed out in the html response without proper output encoding. A simple payload such as <script>alert('Got you!!')</script> will popup an alert window. 
* **Jenkinsfile**: when a Multibranch Pipeline is created in Jenkins, such Jenkinsfile is used as pipeline definition. Any change in the github repo, after properly configuring webhooks, will trigger a build in Jenkins. In my case I was running Jenkins in my local machine, not accessible from the internet, so instead of setting up webhooks I trigger a Scan Repository in Jenkins which looks for changes in the repo and executes the build. AWS required credentials to launch the AWS CLI from Jenkins are configured as credentials, and are available from the Jenkins file thanks to Credentials plugin. 
* folder **media/**: contains some screenshots illustrating how the system reacts on regular payloads and payloads containing an XSS. It also includes a screenshot of a CloudWatch Dashboard when the XSS Blocked Request can be tracked and an alarm set on a certain threshold. 
* folder **utils/**: script to generate some load
* folder **templates/**: contain several AWS CloudFormation templates:
  * **cloudformation_template.json**: initial solution, discarded later. As I was having some trouble with AWS networking, I setup a CDN in front of the webserver with some WAF rules (WebACL). The reason behind that is that the AWS WAF can only be setup on a CLoudFront distribution or on an Application Load Balancer. Even when the solution based on CloudFront was not correct (I was using ip_address.xip.io as Origin, which should have been setup to point to the CloudFront distribution, and the webserver was available anyways, as I was not limiting access to it only via the distribution) at least I could show how AWS WAF, among other interesting functionalities, is able to block _some_ request containing XSS payloads (at least simple ones). 
  * **cloudformation_template_lb.json**: current solution. After solving the networking issues, the CloudFront distribution was removed and an Application Load Balancer (ALB) added instead. 
  * **aws-waf-security-automations.template, aws-waf-security-automations-cloudfront.template, aws-waf-security-automations-alb.template**: a set of parametrized templates which can be nested in the main one to implement the WebACL (set of WAF rules) which can be attached to either a CloudFront distribution or an Application Load Balancer (ALB). Indeed, the first one will nest one of the others, depending on the endpoint type (CloudFront or ALB). Those templates are included only as reference as in the real setup they are stored in an S3 bucket, following the recommendations from [AWS WAF Security Automation Solution](https://aws.amazon.com/solutions/aws-waf-security-automations/)
