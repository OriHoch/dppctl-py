# dppctl pyhton library

## Development Quickstart

* Install Python 3.6

```
pipenv install
pipenv shell
pip install -e .
dppctl
```

## Initializing using minikube

see [dppctl-pipelines](https://github.com/OriHoch/dppctl-pipelines/blob/master/README.md#setting-up-a-local-minikube-cluster) for the required prerequisites

```
dppctl init minikube
```

## Running pipelines

Run from a url zip source - using dppctl-pipelines examples

```
dppctl run --workload https://github.com/OriHoch/dppctl-pipelines/archive/master.zip#examples/noise/workload ./noise
```

## Using the helm provider to run on Kamatera cloud

You need a kamatera-k8s environment with initialized environment, see [kamatera-k8s README](https://github.com/OriHoch/kamatera-k8s/blob/master/README.md#kamatera--kubernetes) for details

We use a custom Dockerfile and entrypoint to demonstrate running dppctl on any kubernetes cluster

Assuming your kamatera-k8s is at ../kamatera-k8s relative to dppctl-py

Set the environment name

```
export KAMATERA_ENVIRONMENT_NAME=your-kamatera-environment-name
```

Initialize dppctl on your kamatera cluster

```
docker run -it -v `pwd`/../kamatera-k8s:/kamatera-k8s -e KAMATERA_ENVIRONMENT_NAME orihoch/dppctl-kamatera init helm
```

Run a workload from the dppctl-pipelines examples

```
docker run -it -v `pwd`/../kamatera-k8s:/kamatera-k8s -e KAMATERA_ENVIRONMENT_NAME orihoch/dppctl-kamatera \
               run --workload=https://github.com/OriHoch/dppctl-pipelines/archive/master.zip#dppctl-pipelines-master/examples/noise/workload \
                   ./noise
```
