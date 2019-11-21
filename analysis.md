# Analysis

## Description

The solution includes a extremely simple PHP application served by an Apache httpd server with php configured running on a Ubuntu system. Both the infrastructure (CloudFormation templates) and the application (php file in src folder) reside in the same repository. Probably it would be a better choice to split them into different ones to avoid checking infrastructure for every single change in the code (as changes in the code will happen more often). 

When setting up properly wehbooks in the github repo, new commits (or PRs, ... depending on the config) those will be triggered against the Jenkins project. The Jenkins project is a Multibranch Pipeline where the job definition is the Jenkinsfile in the repo itself. Such job mainly consist in a set of operations using AWS CLI. Required credentials for AWS CLI are stored safely in Jenkins and made available to the Jenkins job thanks to the credentials plugin. The steps implemented in the Jenkinsfile are the following:
* triggers the CloudFormation template to build the required infrastructure
* query the infrastructure build to obtain the IP addresses of the instantiated webservers. 
* Using scp, copies the php file in src folder to /var/www/html folder in the webservers. Permissions have been adjusted to make that possible. 

The private key required to connect using SSH (scp) are also stored in Jenkins credentials. The corresponding public key is setup in both instances to allow SSH access. 

### Infrastructure

The infrastructure is based on two identical instances of a Ubuntu server running in the same VPC in two different subnets in different Availability Zones. An application load balancer (ALB) is used to distribute requests among the available servers, increasing the global availability of the solution. Even when the instances have public IP addresses, as required to access them using SSH, the HTTP port is only accessible from the ALB and the SSH port access is restricted to the provided range / IP address. Indeed, in the template, by default, the SSH access is open (0.0.0.0/0) but it should not be like that in production, in order to provide a secure by default setup. 

The ALB is equipped with a WebACL made of a set of configurable WAF rules. Among other useful features, such rules contains an XSS filter which is used to block requests containing potential XSS payloads. Of course, a problem such as an XSS, should be fixed in the application, considering the WAF as an additional layer of defense, following the defense in depth principle. Full details available in [AWS WAF Security Automations Solution](https://aws.amazon.com/solutions/aws-waf-security-automations/).

The templates of the WebACL are included for reference but the setup reads such templates from an S3 Bucket. 

An XSS can be avoided using a simpler approach, such as adding some security HTTP Headers, as following: 
`
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'none'
`
Please note CSP policy above is quite restrictive and might need to be extended to allow local image or scripts loading, but will prevent in any case javascript injected directly from a request payload, allowing only javascript loading from a file in an allowed location. 

Although such headers can be setup in the http server config, no need to add them to all files in the application, a WAF is a more complete solution as it provides protections against the following potential threats:
* XSS 
* SQLi
* HTTP Flooding (DDoS, brute force login attempts, ...) 
* Scanners
* IP Reputation lists and Bad Bots 

### Logging and monitoring

The ALB is configured to log all requests to a dedicated S3 Bucket. All requests rejected by the WAF rules (WebACL) return HTTP Status 403. Such status, along with other useful information, is included in the log. Therefore, it is pretty straightforward to use CloudWatch to define a metric and even setup basic alarms based on thresholds, as showed in the following figure
![Monitoring Screenshots](media/monitoring.png)

## Further Improvements

A lot ;) But let us summarize some of them

### TLS Support 

Nowadays, all websites should run only over TLS. Even when there is no confidential information to protect, TLS is recommended as allows clients to verify the server identity. In addition, the corresponding HSTS security header must be added
`
Strict-Transport-Security: max-age=31536000 
`

### Platform running the application 

I would not run an application processing personal data using an image provided by Amazon. I would choose an image which is minimal, ie contains really only the necessary packages to run the application (no apt, no bash, no curl, no wget, ...). Ideally the image could be read only and disposed and recreated from scratch as frequently as possible. 

All those requirements can be met using an infrastructure based on Docker, where we can use a builder image to build the application but a really minimal image (built from distroless or scratch) to run the application. 

All images must be scanned in order to find potential vulnerabilities in any of the components. Such step must be added to the pipeline. 

### Application deployment

In the current setup SSH access is required to deploy the application. Ideally, other solution should be used for the deployment which allows us to complete separate the data plane (clients using the application) from the management plane (application deployment). Looks like AWS CodeDeploy could be a suitable solution, just replacing the EC2 instances by an Auto Scaling group.

### CloudWatch automation

Add CloudWatch Dashboard and alarm creation to the CloudFormation template. 

### Security scans in the pipeline

Apart from scanning the Linux image as mentioned above, the application should be scanned to find potential vulnerabilities in Open Source 3rd party components (not applicable in this case due to the simplicity of the application). 

When possible, if a good tool (good in findings, reduced ratio of false positives) is available, perform a source code static scan.

### Security smoke tests

In the pipeline, after deployment, would be nice to have some security smoke tests (must run fast), eg:
* IP/port scan to ensure server instances can not be reached directly, check ALB exposes only HTTPS port. 
* Ensure S3 buckets are not public
* OWASP ZAP smoke tests

