import pulumi
from pulumi_aws import s3
from components.infra import Infra
from components.service import ServiceDeployment   

# Create base AWS Infrastructutre (VPC, EKS, etc.)
infra = Infra('base-infra')

# Create raw AWS data storage resources
bucket = s3.Bucket('my-bucket')

# Deploy a Kubernetes service into the cluster
service = ServiceDeployment(
    'nginx', 
    {
        'image': 'nginx:1.15.4',
        'resources': {
            'requests': {
                'cpu': '100m',
                'memory': '100Mi'
            }
        },
        'ports': [80],
    }, 
    opts=pulumi.ResourceOptions(provider=infra.k8s_provider)
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export('namespace', infra.namespace.id)
pulumi.export('url', service.service.status)