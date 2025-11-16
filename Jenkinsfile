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

                    # Configure minikube Docker env
                    & minikube -p minikube docker-env | Invoke-Expression

                    # Build and tag image
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest

                    # List images
                    docker images
                """
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                powershell """
                    Write-Output 'Updating Kubernetes manifests...'

                    (Get-Content kubernetes\\deployment.yaml) -replace 'image: ${IMAGE_NAME}:.*', 'image: ${IMAGE_NAME}:${IMAGE_TAG}' | Set-Content kubernetes\\deployment.yaml

                    if (-not (Select-String -Path kubernetes\\deployment.yaml -Pattern 'imagePullPolicy: Never')) {
                        (Get-Content kubernetes\\deployment.yaml) + '        imagePullPolicy: Never' | Set-Content kubernetes\\deployment.yaml        
                    }
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
            echo "Pipeline finished at ${new Date()}"
            powershell "kubectl logs -l app=flask-k8s-app -n ${KUBE_NAMESPACE} --tail=50 || Write-Output 'No logs available'"
        }
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Pipeline failed. Check above logs."
            powershell """
                kubectl get events -n ${KUBE_NAMESPACE} --sort-by='.lastTimestamp' | Select-Object -Last 20
                kubectl get pods -n ${KUBE_NAMESPACE} -o wide
            """
        }
    }
}