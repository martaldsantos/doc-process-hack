
## 1. Manual Setup Environment, on device (Anaconda or venv)

1. Clone the repo

    ```bash
    git clone https://github.com/martaldsantos/doc-process-hack
    ```

1. Open the repo in VS Code

    ```bash
    cd doc-process-hack
    code .
    ```

1. Create a new local Python environment using **either** [anaconda](https://www.anaconda.com/products/individual) **or** [venv](https://docs.python.org/3/library/venv.html) for a managed environment.

    1. **Option 1**: Using anaconda

        ```bash
        conda create -n contoso-chat python=3.11
        conda activate contoso-chat
        pip install -r requirements.txt
        ```

    1. **Option 2:** Using venv

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        ```

## 2. Create Azure resources

We setup our development ennvironment in the previous step. In this step, we'll **provision Azure resources** for our project, ready to use for developing our LLM Application.


### 2.1 Authenticate with Azure

Start by connecting your Visual Studio Code environment to your Azure account:

1. Open the terminal in VS Code and use command `az login`. 
1. Complete the authentication flow. 

Verify that the console shows a message indicating a successful authentication. **Congratulations! Your VS Code session is now connected to your Azure subscription!**

### 2.2 Run Provisioning Script

The project requires a number of Azure resources to be set up, in a specified order. To simplify this, an auto-provisioning script has been provided. (NOTE: It will use the current active subscription to create the resource. If you have multiple subscriptions, use `az account set --subscription "<SUBSCRIPTION-NAME>"` first to set the desired active subscription.)

Run the provisioning script as follows:

  ```bash
  ./provision.sh
  ```
If you get an error of permissions, please firstly run the following code: 

  ```bash
chmod u+r+x provision.sh
  ```

 This run should take a couple of minutes. 
  
The script should **set up a dedicated resource group** with the following resources:

 - **Azure Open AI service** resource
 - **Azure Document Intelligence workspace** resource
 - **Azure AI Search service**  resource
 - **Azure Cosmos DB account** resource
 - **Azure Storage Account**  resource


### 2.3 Verify your resources' creation

Go back to your `Azure Portal` and find your `Resource Group`that should by now contain 5 resources and look like this:

![image](https://github.com/user-attachments/assets/91215492-faaf-4696-aa5c-2b955fb2f7d5)


### 2.4 Verify `.env` setup

The default sample has an `.env.sample` file that shows the relevant environment variables that need to be configured in this project. The script should create a `.env` file that has these same variables _but populated with the right values_ for your Azure resources.

If the file is not created, simply copy over `.env.sample` to `.env` - then populate those values manually from the respective Azure resource pages using the Azure Portal.

