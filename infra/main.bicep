targetScope = 'subscription'

@description('The name of the Resource Group to create.')
param resourceGroupName string

@description('The location for all resources.')
param location string = 'eastus'

@description('The name of the Azure Container Registry. Must be globally unique.')
param acrName string

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
}

module acrModule 'acr.bicep' = {
  scope: rg
  name: 'acrDeployment'
  params: {
    acrName: acrName
    location: location
  }
}

output acrLoginServer string = acrModule.outputs.loginServer
