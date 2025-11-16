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
                        
                        Write-Output 'Listing built images:'
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
                        Write-Output 'Loading image ${IMAGE_NAME}:${IMAGE_TAG} into Minikube...'
                        minikube image load ${IMAGE_NAME}:${IMAGE_TAG}
                        
                        Write-Output 'Loading image ${IMAGE_NAME}:latest into Minikube...'
                        minikube image load ${IMAGE_NAME}:latest
                        
                        Write-Output 'Verifying images with minikube image ls...'
                        minikube image ls | Select-String ${IMAGE_NAME}
                        
                        Write-Output 'Images loaded successfully!'
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes..."
                    powershell """
                        Write-Output 'Applying Kubernetes manifests...'
                        kubectl apply -f kubernetes/
                        
                        Write-Output 'Updating deployment image to ${IMAGE_NAME}:${IMAGE_TAG}...'
                        kubectl set image deployment/flask-deployment flask-container=${IMAGE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                        
                        Write-Output 'Deployment updated successfully!'
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Verifying deployment..."
                    powershell """
                        Write-Output 'Waiting for deployment rollout to complete...'
                        kubectl rollout status deployment/flask-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                        
                        Write-Output ''
                        Write-Output 'Current pods:'
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o wide
                        
                        Write-Output ''
                        Write-Output 'Current services:'
                        kubectl get svc -n ${KUBE_NAMESPACE}
                        
                        Write-Output ''
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
            powershell """
                Write-Output ''
                Write-Output 'Final pod status:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app 2>&1 | Out-String
            """
        }
        success {
            echo "[SUCCESS] Deployment completed successfully!"
            powershell """
                Write-Output '========================================='
                Write-Output '    DEPLOYMENT SUCCESSFUL!'
                Write-Output '========================================='
                Write-Output ''
                Write-Output 'Pods:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o wide
                Write-Output ''
                Write-Output 'Services:'
                kubectl get svc -n ${KUBE_NAMESPACE}
                Write-Output ''
                Write-Output 'Access your application at:'
                minikube service flask-service --url -n ${KUBE_NAMESPACE}
                Write-Output ''
                Write-Output '========================================='
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
            powershell """
                Write-Output '========================================='
                Write-Output '    DEPLOYMENT FAILED - DEBUGGING INFO'
                Write-Output '========================================='
                Write-Output ''
                Write-Output 'Pod Status:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o wide 2>&1 | Out-String
                Write-Output ''
                Write-Output 'Recent Events:'
                kubectl get events -n ${KUBE_NAMESPACE} --sort-by=.lastTimestamp 2>&1 | Select-Object -Last 10
                Write-Output ''
                Write-Output 'Pod Descriptions:'
                \$pods = kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o jsonpath='{.items[*].metadata.name}' 2>&1
                if (\$pods -and \$pods -notmatch 'error') {
                    foreach (\$pod in \$pods.Split()) {
                        if (\$pod) {
                            Write-Output "--- Pod: \$pod ---"
                            kubectl describe pod \$pod -n ${KUBE_NAMESPACE} 2>&1 | Select-Object -Last 20
                        }
                    }
                }
                Write-Output ''
                Write-Output '========================================='
            """
        }
    }
}