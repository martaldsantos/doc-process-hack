
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

1. Install the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) for your device OS

1. Install the [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) in VSCode

1. Install the [Azure Functions Core Tools](https://learn.microsoft.com/en-gb/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp) in VSCode

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

## 4. Create Azure resources

We setup our development ennvironment in the previous step. In this step, we'll **provision Azure resources** for our project, ready to use for developing our LLM Application.


### 4.1 Authenticate with Azure

Start by connecting your Visual Studio Code environment to your Azure account:

1. Open the terminal in VS Code and use command `az login`. 
1. Complete the authentication flow. 

Verify that the console shows a message indicating a successful authentication. **Congratulations! Your VS Code session is now connected to your Azure subscription!**

### 4.2 Run Provisioning Script

The project requires a number of Azure resources to be set up, in a specified order. To simplify this, an auto-provisioning script has been provided. (NOTE: It will use the current active subscription to create the resource. If you have multiple subscriptions, use `az account set --subscription "<SUBSCRIPTION-NAME>"` first to set the desired active subscription.)

Run the provisioning script as follows:

  ```bash
  ./provision.sh
  ```
If you get an error of permissions, please firstly run the following code: 

  ```bash
chmod u+r+x provision.sh
  ```
The script should **set up a dedicated resource group** with the following resources:

 - **Azure AI services** resource
 - **Azure Machine Learning workspace** (Azure AI Project) resource
 - **Search service** (Azure AI Search) resource
 - **Azure Cosmos DB account** resource

The script will set up an **Azure AI Studio** project with the following model deployments created by default, in a relevant region that supports them. _Your Azure subscription must be [enabled for Azure OpenAI access](https://learn.microsoft.com/azure/ai-services/openai/overview#how-do-i-get-access-to-azure-openai)_.
 - gpt-3.5-turbo
 - text-embeddings-ada-002
 - gpt-4

The Azure AI Search resource will have **Semantic Ranker** enabled for this project, which requires the use of a paid tier of that service. It may also be created in a different region, based on availability of that feature.

### 4.3 Verify `config.json` setup

The script should automatically create a `config.json` in your root directory, with the relevant Azure subscription, resource group, and AI workspace properties defined. _These will be made use of by the Azure AI SDK for relevant API interactions with the Azure AI platform later_.

If the config.json file is not created, simply download it from your Azure portal by visiting the _Azure AI project_ resource created, and looking at its Overview page.

### 4.4 Verify `.env` setup

The default sample has an `.env.sample` file that shows the relevant environment variables that need to be configured in this project. The script should create a `.env` file that has these same variables _but populated with the right values_ for your Azure resources.

If the file is not created, simply copy over `.env.sample` to `.env` - then populate those values manually from the respective Azure resource pages using the Azure Portal (for Azure CosmosDB and Azure AI Search) and the Azure AI Studio (for the Azure OpenAI values)

### 4.5 Verify local connections for Prompt Flow

You will need to have your local Prompt Flow extension configured to have the following _connection_ objects set up:
 - `contoso-cosmos` to Azure Cosmos DB endpoint
 - `contoso-search` to Azure AI Search endpoint
 - `aoai-connection` to Azure OpenAI endpoint

Verify if these were created by using the [pf tool](https://microsoft.github.io/promptflow/reference/pf-command-reference.html#pf-connection) from the VS Code terminal as follows:

```bash
pf connection list
```