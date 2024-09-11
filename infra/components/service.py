
import pulumi
from pulumi import ResourceOptions, ComponentResource, Output
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import (
    ContainerArgs,
    ContainerPortArgs,
    PodSpecArgs,
    PodTemplateSpecArgs,
    ResourceRequirementsArgs,
    Service,
    ServicePortArgs,
    ServiceSpecArgs,
)
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from typing import Sequence, TypedDict

class ServiceDeploymentArgs(TypedDict):
    name: str
    '''
    The name of the service
    '''
    image: str
    '''
    The container image to deploy into the K8s deployments
    '''
    resources: ResourceRequirementsArgs
    '''
    The resource requirements for the container
    '''
    replicas: int
    '''
    The number of replicas to deploy
    '''
    ports: Sequence[int]
    '''
    The ports to expose on the service
    '''
    allocate_ip_address: bool
    '''
    Whether to allocate an IP address for the service
    '''
    is_minikube: bool    
    '''
    Whether the cluster is minikube
    '''

class ServiceDeployment(ComponentResource):
    deployment: Deployment
    service: Service
    ip_address: Output[str]

    def __init__(self, name: str, args: ServiceDeploymentArgs = None, opts: ResourceOptions = None):
        super().__init__('k8sx:component:ServiceDeployment', name, {}, opts)

        labels = {"app": name}
        container = ContainerArgs(
            name=name,
            image=args['image'],
            resources=args['resources'] or ResourceRequirementsArgs(
                requests={
                    "cpu": "100m",
                    "memory": "100Mi"
                },
            ),
            ports=[ContainerPortArgs(container_port=p) for p in args['ports']] if args['ports'] else None,
        )
        self.deployment = Deployment(
            name,
            spec=DeploymentSpecArgs(
                selector=LabelSelectorArgs(match_labels=labels),
                replicas=args['replicas'] if 'replicas' in args else 1,
                template=PodTemplateSpecArgs(
                    metadata=ObjectMetaArgs(labels=labels),
                    spec=PodSpecArgs(containers=[container]),
                ),
            ),
            opts=pulumi.ResourceOptions(parent=self))
        self.service = Service(
            name,
            metadata=ObjectMetaArgs(
                name=name,
                labels=self.deployment.metadata.apply(lambda m: m.labels),
            ),
            spec=ServiceSpecArgs(
                ports=[ServicePortArgs(port=p, target_port=p) for p in args['ports']] if 'ports' in args else None,
                selector=self.deployment.spec.apply(lambda s: s.template.metadata.labels),
                type=("ClusterIP" if args['is_minikube'] else "LoadBalancer") if 'allocate_ip_address' in args else None,
            ),
            opts=pulumi.ResourceOptions(parent=self))
        if 'allocate_ip_address' in args:
            if 'is_minikube' in args:
                self.ip_address = self.service.spec.apply(lambda s: s.cluster_ip)
            else:
                ingress=self.service.status.apply(lambda s: s.load_balancer.ingress[0])
                self.ip_address = ingress.apply(lambda i: i.ip or i.hostname or "")
        self.register_outputs({})