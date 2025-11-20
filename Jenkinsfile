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
                        Write-Output 'Checking Minikube status...'
                        \$status = minikube status --format='{{.Host}}'
                        if (\$status -ne 'Running') {
                            Write-Output 'Minikube is not running. Starting Minikube...'
                            minikube start
                            Start-Sleep -Seconds 10
                        }
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
                        Write-Output 'Setting Docker environment to use Minikube...'
                        & minikube -p minikube docker-env --shell powershell | Invoke-Expression
                        
                        Write-Output 'Building Docker image inside Minikube...'
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        
                        Write-Output 'Listing built images:'
                        docker images | Select-String ${IMAGE_NAME}
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
                        
                        Write-Output 'Patching deployment to use IfNotPresent pull policy...'
                        kubectl patch deployment flask-deployment -n ${KUBE_NAMESPACE} -p '{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"flask-container\",\"imagePullPolicy\":\"IfNotPresent\"}]}}}}'
                        
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
            echo "[SUCCESS] Deployment completed successfully!"
            powershell """
                Write-Output '========================================='
                Write-Output '    DEPLOYMENT SUCCESSFUL!'
                Write-Output '========================================='
                Write-Output 'Pods:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o wide
                Write-Output 'Services:'
                kubectl get svc -n ${KUBE_NAMESPACE}
                Write-Output 'Access your application at:'
                minikube service flask-service --url -n ${KUBE_NAMESPACE}
                Write-Output '========================================='
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
        }
    }
}
