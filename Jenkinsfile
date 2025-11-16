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
                        Write-Output "Using KUBECONFIG: ${env:KUBECONFIG}"
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
                        Write-Output 'Applying Kubernetes manifests...'
                        kubectl apply -f kubernetes/
                        
                        Write-Output 'Updating deployment image...'
                        kubectl set image deployment/flask-deployment flask-container=${IMAGE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                        
                        Write-Output 'Deployment updated successfully!'
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Checking rollout status..."
                    powershell """
                        Write-Output 'Waiting for deployment to complete...'
                        kubectl rollout status deployment/flask-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                        
                        Write-Output 'Current pods:'
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o wide
                        
                        Write-Output 'Current services:'
                        kubectl get svc -n ${KUBE_NAMESPACE}
                        
                        Write-Output 'Getting service URL...'
                        minikube service flask-service --url -n ${KUBE_NAMESPACE}
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
                Write-Output 'Deployment Summary:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o wide
                kubectl get svc -n ${KUBE_NAMESPACE}
                Write-Output '=================================='
                Write-Output 'Access your application at:'
                minikube service flask-service --url -n ${KUBE_NAMESPACE}
                Write-Output '=================================='
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed - check logs above"
        }
    }
}