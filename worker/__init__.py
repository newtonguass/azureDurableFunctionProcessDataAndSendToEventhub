# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import time
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential
import os



def getKeyVaultCredentials():
    if  os.environ["env"]!="dev":
        return ManagedIdentityCredential()
    else:
        tenant_id = os.environ["azureTenantID"]
        client_id = os.environ["azureClientID"]
        client_secret = os.environ["azureClientSecret"]
        credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        return credential
def main(name: str) -> str:
    #producer = EventHubProducerClient(fully_qualified_namespace=os.environ["fully_qualified_namespace"],
    #                                eventhub_name=os.environ["eventhub_name"],
    #                                credential=getKeyVaultCredentials())
    print(name)
    return "success"
