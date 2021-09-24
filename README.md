# CodePipeline-selective-trigger
Triggers CodePipeline for folder level changes in repository (Currently supporting BitBucket Cloud)

A lot of organizations use monorepo where they choose to embed multiple applications or services in a single repository separated by folders.
With the default setup in CodePipeline, a release pipeline is invoked whenever a change in the source code repository is detected. That means any commit in the repository will invoke all the pipelines associated with it.

This solution will help to trigger the AWS CodePipelines based on the changes happening on the folders in repo. This solution will dploy below components:
1. API Gateway - To receive BitBucket Webhook events
2. Lambda Function - To detect the folders of the repo where changes has happend and then start the Pipeline execution based on branch and folder where changes occured.

**Pre requisites:**
1. Generate App Password on BitBucket

### Creating an app password - BitBucket
To create an app password:
1. From your avatar in the bottom left, click **Personal settings**.
2. Click **App passwords** under Access management.
3. Click **Create app password**.
4. Give the app password a name related to the application that will use the password.
5. Select the permissions as below:
   - Webhooks Read and Write
   - Repositories Read 
7. Copy the generated password and either record or paste it into the application you want to give access. The password is only displayed this one time.

### Creating a BitBucket webhook
1. Go to the BitBucket repository you want to create webhook with.
2. Go to **Repository Setting**. Click on **Webhooks**.
3. Click on **Add Webhook**.
4. Give Webhook a **Title**.
5. Under **URL** enter the URL of the API Gateway. You can get this from CloudFormation Console, under outputs tab.

### Deploy the Solution
1. Deploy the [CloudFormation](cloudformation//api-lambda.yaml) in AWS Console.
2. Go to Lambda Function deployed by CloudFormation and upload [zip file](lambda/lambda-bitbucket/lambda.zip). (This is required as this package contains requests module of python.)
3. Go to Lambda and do following:
   - Provide username and app password in line number 4 and 5.
   - Modify from Line 35 and add conditions according to your use case.
4. Deploy the Lambda Function.
