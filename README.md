# az-mgmt-app
Azure resources management application by Python.

## Install requirements
```bash
pip install -r requirements.txt
```

## Authentication:
1. Register a AAD application, and create an app secret
2. In the AAD application "API Permission", add "Azure Service Management"
3. In your azure subscription "Access Control(IAM)", add the AAD application to roles assignment with "Contributor" Role

## Azure China Environment: 
Reference: https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-sovereign-domain

## ARM deployment:
Reference: https://github.com/Azure-Samples/Hybrid-Python-Samples/blob/master/TemplateDeployment/deployer.py

