# az-mgmt-app
Azure resources management application by Python.

This application pick up the arm templates in the `templates` folder and deploy the Azure resources with Azure Management API automatically, it support both Azure global and China.

## Install and run
1. Make settings in `settings.yaml`
2. Start deployment
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

## Authentication:
1. Register a AAD application, and create an app secret
2. In the AAD application "API Permission", add "Azure Service Management"
3. In your azure subscription "Access Control(IAM)", add the AAD application to roles assignment with "Contributor" Role

## Azure China Environment: 
Reference: https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-sovereign-domain

## ARM deployment:
Reference: https://github.com/Azure-Samples/Hybrid-Python-Samples/blob/master/TemplateDeployment/deployer.py

