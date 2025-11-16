// Jenkinsfile for CI/CD pipeline
// This pipeline builds a Docker image, deploys to Kubernetes, and verifies deployment
pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "flask-k8s-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBE_NAMESPACE = "default"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                    
                    powershell """
                        Write-Output 'Building Docker image...'
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        docker images | Select-String ${IMAGE_NAME}
                    """
                }
            }
        }
        
        stage('Load Image to Minikube') {
            steps {
                script {
                    echo "Loading image into Minikube..."
                    powershell """
                        Write-Output 'Loading images into Minikube...'
                        minikube image load ${IMAGE_NAME}:${IMAGE_TAG}
                        minikube image load ${IMAGE_NAME}:latest
                        
                        Write-Output 'Verifying images in Minikube...'
                        minikube image ls | Select-String ${IMAGE_NAME}
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Applying Kubernetes manifests..."
                    powershell """
                        kubectl apply -f kubernetes/
                        kubectl set image deployment/flask-k8s-deployment flask-k8s-app=${IMAGE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Checking rollout status..."
                    powershell """
                        kubectl rollout status deployment/flask-k8s-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                        
                        Write-Output 'Current pods:'
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app
                        
                        Write-Output 'Current services:'
                        kubectl get svc -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished at ${new Date()}"
        }
        success {
            echo "[SUCCESS] Deployment successful!"
            powershell """
                Write-Output '=================================='
                Write-Output 'Final Deployment Status:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app -o wide
                kubectl get svc -n ${KUBE_NAMESPACE}
                Write-Output '=================================='
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
            powershell """
                Write-Output 'Recent Events:'
                kubectl get events -n ${KUBE_NAMESPACE} --sort-by=.lastTimestamp | Select-Object -Last 10
                
                Write-Output 'Pod Status:'
                kubectl get pods -n ${KUBE_NAMESPACE}
            """
        }
    }
}