# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
import azure.functions as func
import azure.durable_functions as df
import os
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

def getKeyVaultCredentials():
    if  os.environ["env"]!="dev":
        return ManagedIdentityCredential()
    else:
        tenant_id = os.environ["azureTenantID"]
        client_id = os.environ["azureClientID"]
        client_secret = os.environ["azureClientSecret"]
        credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        return credential

def getPathes(keyId, keySecret):
    return ["test", "test2"]

def orchestrator_function(context: df.DurableOrchestrationContext):
    vaultUrl = os.environ["vaultUrl"]
    secretClient = SecretClient(vault_url=vaultUrl, credential=getKeyVaultCredentials())
    crwdKeyId = secretClient.get_secret(os.environ["crwdKeyId"])
    crwdKeySecret = secretClient.get_secret(os.environ["crwdKeySecret"])
    print(crwdKeyId.value, crwdKeySecret.value)
    parallel_tasks = [ context.call_activity("worker", path) for path in getPathes(crwdKeyId.value, crwdKeySecret.value) ]
    outputs = yield context.task_all(parallel_tasks)
    print(outputs)
    return outputs
    
main = df.Orchestrator.create(orchestrator_function)