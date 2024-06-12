import pulumi
import pulumi_azure_native as azure_native

# Create an Azure Resource Group
resource_group = azure_native.resources.ResourceGroup('resourceGroup')

# Create an Azure Storage Account
storage_account = azure_native.storage.StorageAccount('storageaccount',
    resource_group_name=resource_group.name,
    sku=azure_native.storage.SkuArgs(
        name=azure_native.storage.SkuName.STANDARD_LRS,
    ),
    kind=azure_native.storage.Kind.STORAGE_V2,
)

# Create a Blob Container
blob_container = azure_native.storage.BlobContainer('blobcontainer',
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    public_access=azure_native.storage.PublicAccess.NONE,
)

# Upload a sample file to the Blob Container
blob = azure_native.storage.Blob('samplefile',
    resource_group_name=resource_group.name,
    account_name=storage_account.name,
    container_name=blob_container.name,
    source=pulumi.FileAsset('path/to/samplefile.txt'),
)

# Export the resource group name, storage account name, blob container name, and blob URL
pulumi.export('resource_group_name', resource_group.name)
pulumi.export('storage_account_name', storage_account.name)
pulumi.export('blob_container_name', blob_container.name)
pulumi.export('blob_url', pulumi.Output.concat('https://', storage_account.name, '.blob.core.windows.net/', blob_container.name, '/', blob.name))
