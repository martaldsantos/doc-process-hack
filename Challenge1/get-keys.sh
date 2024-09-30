#!/bin/bash
#
# This script will retrieve necessary keys and properties from Azure Resources 
# deployed using "Deploy to Azure" button and will store them in a file named
# "config.env" in the current directory.

# Login to Azure
if [ -z "$(az account show)" ]; then
  echo "User not signed in Azure. Signin to Azure using 'az login' command."
  az login --use-device-code
fi

# Get the resource group name from the script parameter named resource-group
resourceGroupName=""

# Parse named parameters
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --resource-group) resourceGroupName="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if resourceGroupName is provided
if [ -z "$resourceGroupName" ]; then
    echo "Enter the resource group name where the resources are deployed:"
    read resourceGroupName
fi

# Get resource group deployments, find deployments starting with 'Microsoft.Template' and sort them by timestamp
echo "Getting the deployments in '$resourceGroupName'..."
deploymentName=$(az deployment group list --resource-group $resourceGroupName --query "[?contains(name, 'Microsoft.Template') || contains(name, 'azuredeploy')].{name:name}[0].name" --output tsv)
if [ $? -ne 0 ]; then
	echo "Error occurred while fetching deployments. Exiting..."
	exit 1
fi

# Get output parameters from last deployment to the resource group and store them as variables
echo "Getting the output parameters from the last deployment '$deploymentName' in '$resourceGroupName'..."
az deployment group show --resource-group $resourceGroupName --name $deploymentName --query properties.outputs > tmp_outputs.json
if [ $? -ne 0 ]; then
	echo "Error occurred while fetching the output parameters. Exiting..."
	exit 1
fi

# Extract the resource names from the output parameters
echo "Extracting the resource names from the output parameters..."
cosmosdbAccountName=$(jq -r '.cosmosdbAccountName.value' tmp_outputs.json)
storageAccountName=$(jq -r '.storageAccountName.value' tmp_outputs.json)
documentIntelligenceName=$(jq -r '.documentIntelligenceName.value' tmp_outputs.json)
aiCognitiveServicesName=$(jq -r '.aiCognitiveServicesName.value' tmp_outputs.json)
searchServiceName=$(jq -r '.searchServiceName.value' tmp_outputs.json)

# Delete the temporary file
rm tmp_outputs.json

# Get the keys from the resources
echo "Getting the keys from the resources..."
cosmosdbAccountKey=$(az cosmosdb keys list --name $cosmosdbAccountName --resource-group $resourceGroupName --query primaryMasterKey -o tsv)
cosmosdbEndpoint=$(az cosmosdb show --name $cosmosdbAccountName --resource-group $resourceGroupName --query "documentEndpoint" -o tsv)
storageAccountKey=$(az storage account keys list --account-name $storageAccountName --resource-group $resourceGroupName --query "[0].value" -o tsv)
storageAccountConnectionString=$(az storage account show-connection-string --name $storageAccountName --resource-group $resourceGroupName --query connectionString -o tsv)
documentIntelligenceEndpoint=$(az cognitiveservices account show --name $documentIntelligenceName --resource-group $resourceGroupName --query "properties.endpoints.FormRecognizer" -o tsv)
documentIntelligenceKey=$(az cognitiveservices account keys list --name $documentIntelligenceName --resource-group $resourceGroupName --query key1 -o tsv)
aiCognitiveServicesEndpoint=$(az cognitiveservices account show --name $aiCognitiveServicesName --resource-group $resourceGroupName --query properties.endpoint -o tsv)
aiCognitiveServicesKey=$(az cognitiveservices account keys list --name $aiCognitiveServicesName --resource-group $resourceGroupName --query key1 -o tsv)
searchServiceKey=$(az search admin-key show --resource-group $resourceGroupName --service-name $searchServiceName --query primaryKey -o tsv)

# Overwrite the existing config.env file
if [ -f ../.env ]; then
	rm ../.env
fi

# Store the keys and properties in a file
echo "Storing the keys and properties in '.env' file..."
echo "STORAGE_ACCOUNT_NAME=\"$storageAccountName\"" >> ../.env
echo "STORAGE_KEY=\"$storageAccountKey\"" >> ../.env
echo "STORAGE_CONNECTION_STRING=\"$storageAccountConnectionString\"" >> ../.env
echo "COSMOS_ENDPOINT=\"$cosmosdbEndpoint\"" >> ../.env
echo "COSMOS_KEY=\"$cosmosdbAccountKey\"" >> ../.env
echo "DOC_AI_ENDPOINT=\"$documentIntelligenceEndpoint\"" >> ../.env
echo "DOC_AI_KEY=\"$documentIntelligenceKey\"" >> ../.env
echo "AZURE_OPENAI_ENDPOINT=\"$aiCognitiveServicesEndpoint\"" >> ../.env
echo "AZURE_OPENAI_KEY=\"$aiCognitiveServicesKey\"" >> ../.env
echo "SEARCH_SERVICE_NAME=\"$searchServiceName\"" >> ../.env
echo "SEARCH_ADMIN_KEY=\"$searchServiceKey\"" >> ../.env

echo "Keys and properties are stored in '.env' file successfully."