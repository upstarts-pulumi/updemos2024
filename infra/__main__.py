import pulumi
from pulumi import ResourceOptions, Output
from pulumi_aws import s3
from components.infra import Infra
from components.service import ServiceDeployment   

# Create base AWS Infrastructutre (VPC, EKS, etc.)
infra = Infra('base-infra')

# Create raw AWS data storage resources
bucket = s3.Bucket('my-bucket', acl='private')

# Deploy a Kubernetes service into the cluster
service = ServiceDeployment(
    'app', 
    {
        'image': 'nginx:1.15.4',
        'ports': [80],
        'allocate_ip_address': True,  
    },
    opts=ResourceOptions(provider=infra.k8s_provider)
)

# Export the url for our service
pulumi.export('url', Output.format("http://{}", service.ip_address))