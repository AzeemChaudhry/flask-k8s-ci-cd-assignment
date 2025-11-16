pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "flask-k8s-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBE_NAMESPACE = "default"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code..."
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                powershell """
                    Write-Output 'Building Docker image...'
                    # Configure minikube Docker env for PowerShell
                    minikube -p minikube docker-env --shell powershell | Invoke-Expression
                    # Build and tag image
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    # List images
                    docker images | Select-String ${IMAGE_NAME}
                """
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                powershell """
                    Write-Output 'Updating Kubernetes manifests...'
                    \$content = Get-Content kubernetes\\deployment.yaml -Raw
                    \$content = \$content -replace 'image: ${IMAGE_NAME}:.*', 'image: ${IMAGE_NAME}:${IMAGE_TAG}'
                    \$content | Set-Content kubernetes\\deployment.yaml
                    
                    # Ensure imagePullPolicy is set to Never
                    if (-not (Select-String -Path kubernetes\\deployment.yaml -Pattern 'imagePullPolicy: Never')) {
                        \$content = Get-Content kubernetes\\deployment.yaml -Raw
                        \$content = \$content -replace '(image: ${IMAGE_NAME}:${IMAGE_TAG})', '\$1`n        imagePullPolicy: Never'
                        \$content | Set-Content kubernetes\\deployment.yaml
                    }
                    
                    Write-Output 'Updated deployment.yaml:'
                    Get-Content kubernetes\\deployment.yaml
                """
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                powershell """
                    Write-Output 'Applying Kubernetes manifests...'
                    kubectl apply -f kubernetes/ -n ${KUBE_NAMESPACE}
                    kubectl rollout restart deployment/flask-k8s-deployment -n ${KUBE_NAMESPACE}
                """
            }
        }
        
        stage('Verify Deployment') {
            steps {
                powershell """
                    Write-Output 'Waiting for rollout to complete...'
                    kubectl rollout status deployment/flask-k8s-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                    kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app
                    kubectl get svc -n ${KUBE_NAMESPACE}
                    kubectl describe deployment flask-k8s-deployment -n ${KUBE_NAMESPACE}
                """
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished"
            powershell """
                \$logs = kubectl logs -l app=flask-k8s-app -n ${KUBE_NAMESPACE} --tail=50 2>&1
                if (\$LASTEXITCODE -eq 0) {
                    Write-Output \$logs
                } else {
                    Write-Output 'No logs available yet'
                }
            """
        }
        success {
            echo "[SUCCESS] Deployment successful!"
            powershell """
                Write-Output '=================================='
                Write-Output 'Deployment Summary:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app
                kubectl get svc -n ${KUBE_NAMESPACE}
                Write-Output '=================================='
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed. Check above logs."
            powershell """
                Write-Output 'Recent Kubernetes Events:'
                kubectl get events -n ${KUBE_NAMESPACE} --sort-by='.lastTimestamp' | Select-Object -Last 20
                Write-Output '=================================='
                Write-Output 'Pod Status:'
                kubectl get pods -n ${KUBE_NAMESPACE} -o wide
            """
        }
    }
}