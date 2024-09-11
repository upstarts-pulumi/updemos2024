import pulumi
from pulumi_aws import s3
from pulumi_eks import Cluster
import pulumi_awsx as awsx
import pulumi_eks as eks
import pulumi_kubernetes as k8s

class Infra(pulumi.ComponentResource):
    
    k8s_provider: k8s.Provider
    namespace: k8s.core.v1.Namespace

    def __init__(self, name, vpc_network_cidr="10.0.0.0/16", opts=None):
        super().__init__('contso:infra:Infra', name, None, opts)

        opts = pulumi.ResourceOptions(parent=self)
        
        # Create a unique VPC
        eks_vpc = awsx.ec2.Vpc("eks-vpc",
            enable_dns_hostnames=True,
            cidr_block=vpc_network_cidr,
            tags={"Name": "updemo2024"},
            opts=opts,
        )

        # Create an EKS cluster
        cluster = Cluster('my-cluster',
            vpc_id=eks_vpc.vpc_id,
            subnet_ids=eks_vpc.public_subnet_ids,
            create_oidc_provider=True,
            tags={"Name": "updemo2024"},
            opts=opts,
        )

        # Create a Kubernetes provider for the cluster
        self.k8s_provider = k8s.Provider('k8s-provider', 
            kubeconfig=cluster.kubeconfig,
            opts=opts,
        )

        k8sopts = pulumi.ResourceOptions(parent=self, provider=self.k8s_provider)

        # Create a Kubernetes namespace
        self.namespace = k8s.core.v1.Namespace('app-ns', 
            opts=k8sopts
        )

