#!/bin/bash

# Variables
resourceGroupName="rgweaihack5"
location="swedencentral"  # You can change the region
cosmosAccountName="cosmosweaihack$(openssl rand -hex 3)"
storageAccountName="storageweaihack$(openssl rand -hex 3)"
docAIName="docintel$(openssl rand -hex 3)"  # Random name to ensure uniqueness

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

# Fetch Keys and Endpoint Details
storageKey=$(az storage account keys list --resource-group $resourceGroupName --account-name $storageAccountName --query "[0].value" -o tsv)
cosmosKey=$(az cosmosdb keys list --resource-group $resourceGroupName --name $cosmosAccountName --type keys --query "primaryMasterKey" -o tsv)
docAIKey=$(az cognitiveservices account keys list --name $docAIName --resource-group $resourceGroupName --query "key1" -o tsv)
docAIEndpoint=$(az cognitiveservices account show --name $docAIName --resource-group $resourceGroupName --query "endpoint" -o tsv)

# Set up environment variables in .env file
echo "STORAGE_ACCOUNT_NAME=$storageAccountName" >> .env
echo "STORAGE_KEY=$storageKey" >> .env
echo "STORAGE_CONNECTION_STRING=$storageConnectionString" >> .env
echo "COSMOS_ACCOUNT_NAME=$cosmosAccountName" >> .env
echo "COSMOS_KEY=$cosmosKey" >> .env
echo "DOC_AI_ENDPOINT=$docAIEndpoint" >> .env
echo "DOC_AI_KEY=$docAIKey" >> .env

echo "Provisioning complete!"
