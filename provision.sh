#!/bin/bash

# Variables
resourceGroupName="rgweaihack"
location="swedencentral"  # You can change the region
cosmosAccountName="cosmosweaihack$(openssl rand -hex 3)"
storageAccountName="storageweaihack$(openssl rand -hex 3)"
docAIName="docintel$(openssl rand -hex 3)"  # Random name to ensure uniqueness
openAIName="openaiweaihack$(openssl rand -hex 3)"
searchServiceName="searchweaihack$(openssl rand -hex 3)"

# Login to Azure
if [ -z "$(az account show)" ]; then
  echo "You are not logged in. Please run 'az login' first."
  exit 1
fi

# Display the active subscription
echo "Running provisioning using this subscription:"
az account show --query "{subscriptionId:id, name:name}"

# Create Resource Group
echo "Creating resource group $resourceGroupName in $location..."
az group create --name $resourceGroupName --location $location

# Create Storage Account
echo "Creating Storage Account $storageAccountName..."
az storage account create --name $storageAccountName --resource-group $resourceGroupName --location $location --sku Standard_LRS

# Create Cosmos DB Account
echo "Creating Cosmos DB Account $cosmosAccountName..."
az cosmosdb create --name $cosmosAccountName --resource-group $resourceGroupName --locations regionName=$location failoverPriority=0 isZoneRedundant=False

# Create Azure Document Intelligence (formerly Form Recognizer)
echo "Creating Azure Document Intelligence resource $docAIName..."
az cognitiveservices account create --name $docAIName --resource-group $resourceGroupName --kind FormRecognizer --sku S0 --location $location --yes

# Create Azure OpenAI Resource
echo "Creating Azure OpenAI resource $openAIName..."
az cognitiveservices account create --name $openAIName --resource-group $resourceGroupName --kind OpenAI --sku S0 --location $location --yes

# Create Azure Cognitive Search
echo "Creating Azure Cognitive Search service $searchServiceName..."
az search service create --name $searchServiceName --resource-group $resourceGroupName --sku Basic --location $location

# Fetch Keys and Endpoint Details
storageKey=$(az storage account keys list --resource-group $resourceGroupName --account-name $storageAccountName --query "[0].value" -o tsv)
storageConnectionString=$(az storage account show-connection-string --resource-group $resourceGroupName --name $storageAccountName --query "connectionString" -o tsv)
cosmosKey=$(az cosmosdb keys list --resource-group $resourceGroupName --name $cosmosAccountName --type keys --query "primaryMasterKey" -o tsv)
docAIKey=$(az cognitiveservices account keys list --name $docAIName --resource-group $resourceGroupName --query "key1" -o tsv)
docAIEndpoint=$(az cognitiveservices account show --name $docAIName --resource-group $resourceGroupName --query "properties.endpoint" -o tsv)
openAIKey=$(az cognitiveservices account keys list --name $openAIName --resource-group $resourceGroupName --query "key1" -o tsv)
openAIEndpoint=$(az cognitiveservices account show --name $openAIName --resource-group $resourceGroupName --query "properties.endpoint" -o tsv)
searchAdminKey=$(az search admin-key show --resource-group $resourceGroupName --service-name $searchServiceName --query "primaryKey" -o tsv)

# Set up environment variables in .env file with quotation marks
echo "STORAGE_ACCOUNT_NAME=\"$storageAccountName\"" >> .env
echo "STORAGE_KEY=\"$storageKey\"" >> .env
echo "STORAGE_CONNECTION_STRING=\"$storageConnectionString\"" >> .env
echo "COSMOS_ACCOUNT_NAME=\"$cosmosAccountName\"" >> .env
echo "COSMOS_KEY=\"$cosmosKey\"" >> .env
echo "DOC_AI_ENDPOINT=\"$docAIEndpoint\"" >> .env
echo "DOC_AI_KEY=\"$docAIKey\"" >> .env
echo "OPENAI_ENDPOINT=\"$openAIEndpoint\"" >> .env
echo "OPENAI_KEY=\"$openAIKey\"" >> .env
echo "SEARCH_SERVICE_NAME=\"$searchServiceName\"" >> .env
echo "SEARCH_ADMIN_KEY=\"$searchAdminKey\"" >> .env


echo "Provisioning complete!"
