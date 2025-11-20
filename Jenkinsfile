pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "flask-k8s-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBE_NAMESPACE = "default"
        KUBECONFIG = "C:\\Users\\Azeem\\.kube\\config"
    }
    
    stages {
        stage('Verify Kubernetes Connection') {
            steps {
                script {
                    echo "Verifying Kubernetes connection..."
                    powershell """
                        Write-Output 'Testing connection:'
                        kubectl get nodes
                    """
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                    
                    powershell """
                        Write-Output 'Building Docker image...'
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        docker images | Select-String ${IMAGE_NAME} | Select-Object -First 3
                    """
                }
            }
        }
        
        stage('Load Image to Minikube') {
            steps {
                script {
                    echo "Loading images into Minikube..."
                    powershell """
                        Write-Output 'Loading ${IMAGE_NAME}:${IMAGE_TAG}...'
                        minikube image load ${IMAGE_NAME}:${IMAGE_TAG} --daemon
                        
                        Write-Output 'Loading ${IMAGE_NAME}:latest...'
                        minikube image load ${IMAGE_NAME}:latest --daemon
                        
                        Start-Sleep -Seconds 3
                        Write-Output 'Images loaded!'
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes..."
                    powershell """
                        kubectl apply -f kubernetes/
                        kubectl set image deployment/flask-deployment flask-container=${IMAGE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Verifying deployment..."
                    powershell """
                        kubectl rollout status deployment/flask-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app
                        kubectl get svc -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "[SUCCESS] Deployment completed!"
            powershell """
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app
                minikube service flask-service --url -n ${KUBE_NAMESPACE}
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
        }
    }
}
