# pe-python-logging


A wrapper for the python standard `logging` library that eases creation of loggers for use in distributed systems. 

## How to Use

Want to use the plogging wrapper in your project? The code is available as a built distribution from the private Project Eaden Code Artifactory, hosted in AWS. There are a couple steps needed to include it as a base dependency of your project, which vary depending on the platform your project is intended for.

### Local Use Only
This section describes setting up a local project so that you can make use of plogging. This section also applies for remote projects where local testing is necessary (so basically all projects). This is in case the project template automated setup failed.

If you followed the python project creation workflow described in the [project-template]() README, then you should already have a Makefile with the base commands included. 
At the bottom of the variables section of the Makefile (all-caps assignment statements) add the following statement:

```Make
PLOGGING_CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain projecteaden --domain-owner 186292285156 --region eu-west-1 --query authorizationToken --output text --profile $(AWS_PROFILE_NAME)`
```

This automatically fetches the credentials necessary to access the repository. Make sure that you have your `AWS_PROFILE_NAME` set to the name of your AWS SSO profile on your machine.

Then, in order to feed these credentials to pip, you have to modify the `setup-env` rule with the following:

```Makefile
setup-env:
	python3 -m venv env; \
	source env/bin/activate; \
	PLOGGING_CODEARTIFACT_AUTH_TOKEN=${PLOGGING_CODEARTIFACT_AUTH_TOKEN} python -m pip install -r requirements.txt -r requirements-dev.txt \
```

Finally, before your run this rule through make, you should modify the project's `requirements.txt` file, adding the following lines **at the bottom**.

```Make
# Make sure that these two lines go at the bottom!
--index-url https://aws:${CODEARTIFACT_AUTH_TOKEN}@projecteaden-186292285156.d.codeartifact.eu-west-1.amazonaws.com/pypi/plogging/simple/
plogging==0.1.1
```

### AWS
In the case that you're deploying/running your project on AWS resources, make sure that those resources have the correct IAM roles to access the code through CodeArtifact, specifically:

```json

```