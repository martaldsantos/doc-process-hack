# Challenge 05: Set up CI/CD for Azure Function

**Expected Duration:** 30 minutes

## Introduction
Your goal in this challenge is to set up a CI/CD pipeline for the Azure Function created in Challenge 4. You will use GitHub Actions to automate the deployment of the Azure Function to the Azure Function App.
By completing this challenge, you will have a fully automated deployment process for the Azure Function.

## Setting up CI/CD for Azure Function

1. Navigate to the Azure Portal and open the Azure Function App created in Challenge 1.
2. Validate that all the necessary Environment variables are set in the Azure Function App. They should be the same as the ones set in the local.settings.json file, which we uploaded to the Azure Function App in Challenge 4.
2. Click on the deployment center and select the source control option, in our case it should be GitHub.
3. Authorize the connection between Azure and GitHub.
4. Select the repository and branch that contains the Azure Function code. (should be your Fork and the branch you're currently using)
5. Select Add a workflow.
6. Select User-assigned identity as the authentication method.
7. Select the User-assigned identity created in Challenge 1.
8. Preview the file, close and click Save.

At this point, you should have a GitHub Action workflow file in your repository. This file will be triggered every time you push changes to your repository. The workflow will build and deploy the Azure Function to the Azure Function App.

You should have as well the necessary secrets added to your repository automatically to authenticate the deployment to Azure.

![alt text](image.png)

Now before you push any new changes to the repository to trigger the workflow, you need to update the GH YAML file with the path to the Azure Function code. By default, the path is set to the repository root which is not our case.

Update the `AZURE_FUNCTIONAPP_PACKAGE_PATH` variable in the YAML file with the path to the Azure Function code in your repository which should be `Challenge4/az-function`.
```yaml
env:
  AZURE_FUNCTIONAPP_PACKAGE_PATH: '.' # set this to the path to your web app project, defaults to the repository root
  PYTHON_VERSION: '3.11' # set this to the python version to use (supports 3.6, 3.7, 3.8)
```

Push some test changes to the repository and check the GitHub Actions tab to see the workflow running.

## Time for Testing! 

Great! Now that we've put in all the work, let's roll the ball! 

1. Download the files that are inside the `Data` folder inside this Challenge. As the name entails, you have 3 different types of documents, and you will need to upload it into the right folder.
2. In your `Azure Portal` open the Azure Function App and on your right hand side you can see an `Invocation` button and open the `Logs` tab. 
3. In another tab, go back to your `Storage Account` and upload your files to their respective folders.
4. Now move back to the `Logs` tab inside your Function App and watch the magic happen. Give it some time to process all the information.
5. Last, and especially, not least, open in another tab your Azure Cosmos DB account, a check if your data is being added to the Database.
