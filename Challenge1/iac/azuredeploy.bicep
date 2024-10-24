@allowed([
  'swedencentral'
])
@description('Azure location where resources should be deployed (e.g., swedencentral)')
param location string = 'swedencentral'

@allowed([
  'westeurope'
])
@description('Azure location where Azure Document Intelligence should be deployed (e.g., westeurope)')
param locationDocumentIntelligence string = 'westeurope' // West Europe hast the latest models needed for Document Intelligence


var prefix = 'hackdocs'
var suffix = uniqueString(resourceGroup().id)

/*
  Create a Cosmos DB account with a database and a container
*/

var databaseAccountName = '${prefix}-cosmosdb-${suffix}'
var databaseName = 'ContosoDB'
var databaseContainerNames = ['PayStubs', 'LoanForms', 'LoanAgreements']

var locations = [
  {
    locationName: location
    failoverPriority: 0
    isZoneRedundant: false
  }
]

resource databaseAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: databaseAccountName
  kind: 'GlobalDocumentDB'
  location: location
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: locations
    databaseAccountOfferType: 'Standard'
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  name: databaseName
  parent: databaseAccount
  properties: {
    resource: {
      id: databaseName
    }
  }
}

resource databaseContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = [for containerName in databaseContainerNames: {
  name: containerName
  parent: database
  properties: {
    resource: {
      id: containerName
      partitionKey: {
        paths: [
          '/id'
        ]
        kind: 'Hash'
      }
    }
    options: {
      autoscaleSettings: {
        maxThroughput: 1000
      }
    }
  }
}]

/*
  Create Storage Account
*/

var storageAccountName = replace('${prefix}-sa-${suffix}', '-', '')

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

/*
  Create Azure Function
*/

var functionHostingPlanName = '${prefix}-function-asp-${suffix}'
var functionAppName = '${prefix}-function-${suffix}'
var functionLogAnalyticsWorkspaceName = '${prefix}-loganalytics-${suffix}'
var functionApplicationInsightsName = '${prefix}-appinsights-${suffix}'

resource functionLogAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: functionLogAnalyticsWorkspaceName
  location: location
  properties: any({
    retentionInDays: 30
    features: {
      searchVersion: 1
    }
    sku: {
      name: 'PerGB2018'
    }
  })
}

resource functionApplicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: functionApplicationInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: functionLogAnalyticsWorkspace.id
  }
}

resource functionHostingPlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: functionHostingPlanName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: true
  }
}

resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: functionHostingPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(functionAppName)
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'APPINSIGHTS_CONNECTION_STRING'
          value: functionApplicationInsights.properties.ConnectionString
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
      cors: {
        allowedOrigins: [
          '*'
        ]
      }
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      use32BitWorkerProcess: false
      linuxFxVersion: 'PYTHON|3.11'
    }
    
    httpsOnly: true
  }
}   

var umiName = '${functionAppName}-umi'
resource functionUmi 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: umiName
  location: 'westeurope' //Region that allows federated creds for deployment
}

/* 
  Create Azure OpenAI Cognitive Services
*/

var aiCognitiveServicesName = '${prefix}-aiservices-${suffix}'

resource aiCognitiveServices 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: aiCognitiveServicesName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'OpenAI'
  properties: {
    apiProperties: {
      statisticsEnabled: false
    }
  }
}

resource aiCognitiveServicesDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  name: 'gpt-4o'
  parent: aiCognitiveServices
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-08-06'
    }
  }
  sku: {
    name: 'GlobalStandard'
    capacity: 100
  }
}

/*
  Create Azure Document Intelligence
*/

var documentIntelligenceName = '${prefix}-di-${suffix}'

resource documentIntelligence 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: documentIntelligenceName
  location: locationDocumentIntelligence
  sku: {
    name: 'S0'
  }
  kind: 'FormRecognizer'
  properties: {
    customSubDomainName: documentIntelligenceName
    apiProperties: {
      statisticsEnabled: false
    }
  }
}

/*
  Create Azure AI Search
*/

var searchServiceName = '${prefix}-search-${suffix}'

resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    hostingMode: 'default'
  }
  dependsOn: [
    aiCognitiveServices
  ]
}

/*
  Return output values
*/

output storageAccountName string = storageAccountName
output cosmosdbAccountName string = databaseAccountName
output documentIntelligenceName string = documentIntelligenceName
output aiCognitiveServicesName string = aiCognitiveServicesName
output searchServiceName string = searchServiceName
