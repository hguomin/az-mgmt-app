# pip install -r requirements.txt

# Authentication:
# 1. Register a AAD application
# 2. In the AAD application "API Permission", add "Azure Service Management"
# 3. In your azure subscription "Access Control(IAM)", add the AAD application to roles assignment with "Contributor" Role

# Azure China Environment: 
# https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-sovereign-domain

# ARM deployment:
# https://github.com/Azure-Samples/Hybrid-Python-Samples/blob/master/TemplateDeployment/deployer.py

import os
import json
import time
import yaml

from msrestazure.azure_cloud import AZURE_CHINA_CLOUD as CLOUD

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import Deployment
from azure.mgmt.resource.resources.models import DeploymentProperties
from azure.mgmt.resource.resources.models import DeploymentMode

from azure.identity import ClientSecretCredential
from azure.identity._constants import AzureAuthorityHosts

def read_yaml(path):
    with open(path, "r") as fd:
        return yaml.safe_load(fd)

def get_app_dir():
    return os.path.join(os.path.dirname(__file__))

def main():
    app_dir = get_app_dir()
    settings = read_yaml(os.path.join(app_dir, "settings.yaml"))

    azure_settings = settings["azure"]
    proj_settings = settings["project"]

    resource_group = proj_settings["name"] + "-rg"
    parameters = {
        "projectName": { 
            "value": proj_settings["name"] 
        },
        "adminUserName": {
            "value": proj_settings["admin"]["username"]
        },
        "adminPassword": {
            "value": proj_settings["admin"]["password"]
        }
    }

    template_path = os.path.join(os.path.dirname(__file__), "templates", "iot-sln.json")
    template = ""
    with open(template_path, "r", encoding="utf-8") as fd:
        template = json.load(fd)

    deployment_properties = DeploymentProperties(mode=DeploymentMode.incremental, template=template, parameters=parameters) 

    credential = ClientSecretCredential(tenant_id=azure_settings["tenant_id"], 
                                        client_id=azure_settings["client_id"], 
                                        client_secret=azure_settings["client_secret"], 
                                        authority=AzureAuthorityHosts.AZURE_CHINA)

    resource_client = ResourceManagementClient(credential=credential, 
                                                subscription_id=azure_settings["subscription_id"], 
                                                base_url=CLOUD.endpoints.resource_manager,
                                                credential_scopes=[CLOUD.endpoints.resource_manager + "/.default"])

    rg_result = resource_client.resource_groups.create_or_update(resource_group, { "location": azure_settings["deployment"]["location"] })

    print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")

    try:
        deployment_async_operation = resource_client.deployments.begin_create_or_update(resource_group, "az-iot-deployment", Deployment(properties=deployment_properties))
        # deployment_async_operation.wait()
        print("Deployment is started.")
        second = 1
        
        while not deployment_async_operation.done():
            print(f"{second}", end='.')
            time.sleep(1)
            second = second + 1
        
        print("\nDeploymnet is finished.")

    except Exception as e:
        print(f"Error occured: {e}")

        print(f"\nDeleting: {resource_group}")
        resource_client.resource_groups.begin_delete(resource_group).result()
        
if __name__=="__main__":
    main()