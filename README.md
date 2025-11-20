# Flask Kubernetes CI/CD Pipeline

Complete CI/CD pipeline using GitHub Flow, Docker, Kubernetes (Minikube), and Jenkins.

This project implements a production-style CI/CD workflow for deploying a **Flask** web application to a **Kubernetes** cluster using **Jenkins**, automated rollouts, and container-orchestration best practices. It follows a multi-task academic assignment that focuses on DevOps, Git branching, and cloud-native deployment.

---

## Project Overview

This repository contains:

* A **Flask** application containerized using **Docker**
* **Kubernetes** Deployment and Service manifests
* A **Jenkins** declarative pipeline for automated delivery
* GitHub branching + PR workflow for collaborative development
* **Minikube**-based Kubernetes environment for local testing
* End-to-end CI/CD integration with automated rollout verification

---

## Architecture Summary

**Tools & Technologies Used**

| Component             | Purpose                                 |
| --------------------- | --------------------------------------- |
| Python (Flask)        | Web application                         |
| Docker                | Containerization                        |
| Minikube / Kubernetes | Orchestration, rollouts, scaling        |
| Jenkins               | Continuous Delivery (CD)                |
| GitHub                | Version control, branching, PR workflow |
| kubectl               | Deployment management                   |

---

## Kubernetes Features Used

### Deployment (`flask-k8s-deployment`)

* Rolling update strategy (safe, zero-downtime updates)
* Replica management for scaling
* Self-healing via ReplicaSet
* `imagePullPolicy` configured for local Minikube usage

### Service (ClusterIP / NodePort depending on task)

Used for:

* Internal load balancing
* Service discovery
* Routing traffic to Pods

### Load Balancing

Kubernetes Services distribute traffic across all replicas automatically

### Horizontal Scaling

Scale replicas with:

```bash
kubectl scale deployment flask-k8s-deployment --replicas=5
```

### Automated Rollouts

Kubernetes performs rolling updates and supports rollback:

```bash
kubectl rollout status deployment/flask-k8s-deployment
kubectl rollout undo deployment/flask-k8s-deployment
```

---

## Running the Application Locally (Docker)

1. **Build the Docker image**

```bash
docker build -t flask-k8s-app:latest .
```

2. **Run the container**

```bash
docker run -p 5000:5000 flask-k8s-app:latest
```

The app will be available at: `http://localhost:5000`

---

## Deploying to Kubernetes (Without Jenkins)

1. **Start Minikube**

```bash
minikube start
```

2. **Load Docker image into Minikube**

```bash
minikube image load flask-k8s-app:latest
```

3. **Apply Kubernetes manifests**

```bash
kubectl apply -f kubernetes/
```

4. **Verify resources**

```bash
kubectl get pods
kubectl get svc
kubectl get deployments
```

---

## CI/CD Pipeline – Jenkins Deployment Workflow

The `Jenkinsfile` automates the Kubernetes deployment using three stages.

### Stage 1 — Build Docker Image

Jenkins builds the Docker image directly from the repository:

```groovy
sh "docker build -t flask-k8s-app:latest ."
```

### Stage 2 — Deploy to Kubernetes

Applies the manifests inside `kubernetes/`:

```groovy
sh "kubectl apply -f kubernetes/"
```

### Stage 3 — Verify Deployment

Ensures rollout success and fetches cluster status:

```groovy
sh "kubectl rollout status deployment/flask-k8s-deployment"
sh "kubectl get pods"
sh "kubectl get svc"
```

---

## How the Jenkins Pipeline Works

1. Admin merges `develop` → `main`.
2. Jenkins auto-triggers (webhook or manual run).
3. Jenkins pulls the repo and reads the `Jenkinsfile`.
4. Image is built → deployed → verified.
5. Kubernetes performs automatic rolling updates.

---

## Git Branching Model

| Purpose                      | Branch                           |
| ---------------------------- | -------------------------------- |
| Main production-ready branch | `main`                           |
| Integration branch           | `develop`                        |
| Feature development          | `feature/*`                      |
| PR-based merging             | Developer → Admin → develop/main |

Each task followed this Git workflow.

---


## End-to-End Pipeline Verification

After merging `feature/final-touch` → `main`, team verification included:

* Docker image builds successfully
* Kubernetes manifests deploy without errors
* Jenkins pipeline triggers and deploys automatically
* Rollout status is successful
* Pods, services, and deployments are active in Minikube
* Full pipeline works: GitHub → Jenkins → Kubernetes



## Conclusion

This project demonstrates a fully functional Cloud-Native CI/CD pipeline integrating:

* GitHub PR workflow
* Docker containerization
* Kubernetes orchestration
* Jenkins automated deployment
* Rolling updates, scaling, load balancing

The system mimics a real-world production DevOps environment.
