Fission Installation with KIND, Helm, Kafka (via Strimzi), and Fission Specs
This README provides step-by-step instructions for setting up a local Kubernetes cluster using KIND, installing Helm, deploying Apache Kafka with the Strimzi operator, and installing Fission, a serverless framework for Kubernetes. It also covers how to create and use Fission specs for managing Fission resources. The setup is designed for development and testing purposes.
Prerequisites
Before starting, ensure you have the following tools installed on your system:

Docker: To run KIND and containerized services.
kubectl: Kubernetes command-line tool to interact with the cluster.
kind: To create a local Kubernetes cluster.
helm: To install Strimzi, Fission, and other Helm charts.
git: To clone repositories.
fission CLI: To interact with Fission (installed later in the process).

Verify installations:
docker --version
kubectl version --client
kind version
helm version
git --version

Step 1: Set Up KIND Cluster
KIND (Kubernetes IN Docker) creates a local Kubernetes cluster for development.

Create a KIND cluster:
kind create cluster --name fission-cluster


Verify the cluster:
kubectl cluster-info --context kind-fission-cluster
kubectl get nodes

This should show a single control-plane node running.


Step 2: Install Helm
Helm is a package manager for Kubernetes, used to install Strimzi and Fission.

Install Helm (if not already installed):
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash


Verify Helm installation:
helm version


Add required Helm repositories:
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add strimzi https://strimzi.io/charts/
helm repo add fission-charts https://fission.io/charts
helm repo update



Step 3: Install Kafka with Strimzi
Strimzi simplifies running Apache Kafka on Kubernetes by providing a Kubernetes operator.

Create a namespace for Kafka:
kubectl create namespace kafka


Install Strimzi Kafka Operator:
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --version 0.45.0


Verify Strimzi installation:
kubectl get pods -n kafka

Look for the strimzi-cluster-operator pod in the Running state.

Deploy a Kafka cluster:Create a file named kafka-cluster.yaml with the following content:
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.9.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
    storage:
      type: ephemeral
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}

Apply the Kafka cluster configuration:
kubectl apply -f kafka-cluster.yaml -n kafka


Verify Kafka cluster:
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
kubectl get pods -n kafka

You should see pods for Kafka and ZooKeeper in the Running state.

Create Kafka topics (for Fission Kafka triggers):Create topic configurations for request-topic, response-topic, and error-topic. Save the following as kafka-topics.yaml:
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: request-topic
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 1
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: response-topic
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 1
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: error-topic
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 1

Apply the topics:
kubectl apply -f kafka-topics.yaml -n kafka


Verify topics:
kubectl get kafkatopics -n kafka



Step 4: Install KEDA
KEDA (Kubernetes Event-Driven Autoscaling) is required for Fission's Kafka trigger to scale functions based on Kafka events.

Create a namespace for KEDA:
kubectl create namespace keda


Install KEDA:
helm install keda kedacore/keda --namespace keda


Verify KEDA installation:
kubectl get pods -n keda

Look for the keda-operator and keda-metrics-apiserver pods in the Running state.


Step 5: Install Fission
Fission is a serverless framework that allows you to deploy functions triggered by events, such as Kafka messages.

Create a namespace for Fission:
kubectl create namespace fission


Install Fission using Helm:
helm install fission fission-charts/fission-all --namespace fission --set kafka.enabled=true --set kafka.brokers="my-cluster-kafka-brokers.kafka.svc:9092"

The --set kafka.enabled=true and --set kafka.brokers options enable Kafka message queue triggers and point to the Kafka brokers.

Verify Fission installation:
kubectl get pods -n fission

Look for pods like controller, executor, and mqtrigger-kafka in the Running state.

Install Fission CLI:Download and install the Fission CLI for your operating system:
curl -Lo fission https://github.com/fission/fission/releases/download/v1.23.0/fission-v1.23.0-linux-amd64
chmod +x fission
sudo mv fission /usr/local/bin/


Verify Fission CLI:
fission version



Step 6: Understanding and Using Fission Specs
Fission specs are YAML files that define Fission resources (e.g., functions, environments, triggers) in a declarative way. Specs allow you to manage Fission resources as code, enabling version control and reproducible deployments.
Key Fission Spec Resources

Environment: Defines the runtime environment for functions (e.g., Node.js, Python, Go).
Function: Defines the serverless function, including its code and entry point.
Package: Bundles the function code and its dependencies.
MessageQueueTrigger: Connects a function to a Kafka topic for event-driven execution.

Example: Creating a Fission Spec

Create a directory for specs:
mkdir fission-specs
cd fission-specs


Define an environment:Create a file named env.yaml:
apiVersion: fission.io/v1
kind: Environment
metadata:
  name: nodejs
  namespace: default
spec:
  runtime:
    image: ghcr.io/fission/node-env:1.23
  builder:
    image: ghcr.io/fission/node-builder:1.23


Define a function:Create a file named function.yaml for a Node.js consumer function that processes Kafka messages:
apiVersion: fission.io/v1
kind: Function
metadata:
  name: kafka-consumer
  namespace: default
spec:
  environment:
    name: nodejs
    namespace: default
  package:
    packageref:
      namespace: default
      name: kafka-consumer-package
  invokeStrategy:
    executionStrategy:
      executorType: newdeploy
      minScale: 1
      maxScale: 3


Define a package:Create a file named package.yaml to bundle the function code:
apiVersion: fission.io/v1
kind: Package
metadata:
  name: kafka-consumer-package
  namespace: default
spec:
  environment:
    name: nodejs
    namespace: default
  source:
    type: literal
    literal: |
      module.exports = async function (context) {
        console.log(context.request.body);
        let obj = context.request.body;
        return {
          status: 200,
          body: "Consumer Response " + JSON.stringify(obj),
        };
      };


Define a Kafka trigger:Create a file named mqtrigger.yaml to connect the function to a Kafka topic:
apiVersion: fission.io/v1
kind: MessageQueueTrigger
metadata:
  name: kafka-trigger
  namespace: default
spec:
  functionref:
    name: kafka-consumer
    namespace: default
  messageQueueType: kafka
  topic: request-topic
  respTopic: response-topic
  errorTopic: error-topic
  maxRetries: 3
  contentType: application/json
  pollingInterval: 100


Apply the specs:
fission spec init
fission spec apply

The fission spec init command creates a fission.yaml file to track specs, and fission spec apply deploys all resources defined in the YAML files.

Verify deployment:
fission fn list
fission mqt list

You should see the kafka-consumer function and kafka-trigger message queue trigger.


Testing the Setup

Create a producer function:Create a simple Go-based producer function to send messages to the Kafka topic. Save the following as producer.go:
package main

import (
    "context"
    "github.com/Shopify/sarama"
    "log"
)

func Handler(ctx context.Context) string {
    config := sarama.NewConfig()
    producer, err := sarama.NewSyncProducer([]string{"my-cluster-kafka-brokers.kafka.svc:9092"}, config)
    if err != nil {
        log.Fatalf("Failed to create producer: %v", err)
    }
    defer producer.Close()

    msg := &sarama.ProducerMessage{
        Topic: "request-topic",
        Value: sarama.StringEncoder("Test message"),
    }

    _, _, err = producer.SendMessage(msg)
    if err != nil {
        log.Fatalf("Failed to send message: %v", err)
    }

    return "Message sent to Kafka!"
}


Package and deploy the producer:
mkdir producer && cd producer
mv ../producer.go .
go mod init producer
go mod tidy
zip -qr producer.zip *
fission env create --name go --image ghcr.io/fission/go-env-1.23 --builder ghcr.io/fission/go-builder-1.23
fission package create --env go --src producer.zip
fission fn create --name producer --env go --pkg producer-zip --entrypoint Handler


Test the producer:
fission fn test --name producer


Verify consumer response:Check the Kafka response-topic for the consumer's output:
kubectl run kafka-consumer-pod -ti --image=quay.io/strimzi/kafka:0.45.0-kafka-3.9.0 --rm=true --restart=Never --namespace kafka -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-brokers.kafka.svc:9092 --topic response-topic

You should see messages like "Consumer Response {\"message\":\"Test message\"}".


Troubleshooting

Pods not starting: Check pod logs using kubectl logs <pod-name> -n <namespace>.
Kafka connection issues: Ensure the Kafka broker address (my-cluster-kafka-brokers.kafka.svc:9092) is correct and reachable.
Fission spec errors: Validate YAML syntax and ensure all referenced resources (e.g., environments, packages) exist.
KEDA scaling issues: Verify KEDA is running and the Kafka trigger is correctly configured.

Cleanup
To delete the setup:
kind delete cluster --name fission-cluster

References

Fission Documentation
Strimzi Documentation
KEDA Documentation
KIND Documentation
Helm Documentation

This setup provides a complete environment for developing and testing serverless functions with Fission, integrated with Kafka for event-driven workloads.
