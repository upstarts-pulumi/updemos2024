import pulumi
from pulumi import ResourceOptions
from pulumi_aws import s3
from components.infra import Infra
from components.service import ServiceDeployment   

# Create base AWS Infrastructutre (VPC, EKS, etc.)
infra = Infra('base-infra')

# Create raw AWS data storage resources
bucket = s3.Bucket('my-bucket')

# Deploy a Kubernetes service into the cluster
service = ServiceDeployment(
    'app', 
    {
        'image': 'nginx:1.15.4',
        'ports': [80],
    }, 
    opts=ResourceOptions(provider=infra.k8s_provider)
)

# Export the name of the bucket
pulumi.export('url', service.service.status)