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
        
        stage('Build Docker Image in Minikube') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG} directly in Minikube..."
                    
                    powershell """
                        Write-Output 'Setting Minikube Docker environment...'
                        & minikube -p minikube docker-env --shell powershell | Invoke-Expression
                        
                        Write-Output 'Building Docker image in Minikube Docker daemon...'
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        
                        Write-Output 'Verifying images in Minikube:'
                        docker images | Select-String ${IMAGE_NAME} | Select-Object -First 3
                    """
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    echo "Updating Kubernetes deployment manifests..."
                    powershell """
                        \$deploymentFile = "kubernetes/deployment.yaml"
                        
                        if (Test-Path \$deploymentFile) {
                            \$content = Get-Content \$deploymentFile -Raw
                            
                            # Update imagePullPolicy to Never if not already set
                            if (\$content -notmatch 'imagePullPolicy:\\s*Never') {
                                \$content = \$content -replace '(image:\\s*${IMAGE_NAME}:.*)', '\$1`n        imagePullPolicy: Never'
                                Set-Content \$deploymentFile \$content
                                Write-Output 'Updated imagePullPolicy to Never'
                            } else {
                                Write-Output 'imagePullPolicy already set to Never'
                            }
                        }
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
                        
                        Write-Output 'Updating deployment image...'
                        kubectl set image deployment/flask-deployment flask-container=${IMAGE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                        
                        Write-Output 'Patching deployment to use imagePullPolicy: Never...'
                        kubectl patch deployment flask-deployment -n ${KUBE_NAMESPACE} -p '{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"flask-container\",\"imagePullPolicy\":\"Never\"}]}}}}'
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            retry(2) {
                steps {
                    script {
                        echo "Verifying deployment (with retry)..."
                        powershell """
                            Write-Output 'Waiting for deployment rollout...'
                            kubectl rollout status deployment/flask-deployment -n ${KUBE_NAMESPACE} --timeout=3m
                            
                            Write-Output 'Checking pod status...'
                            kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app
                            
                            Write-Output 'Checking services...'
                            kubectl get svc -n ${KUBE_NAMESPACE}
                        """
                    }
                }
            }
        }
        
        stage('Health Check') {
            retry(2) {
                steps {
                    script {
                        echo "Performing health check (with retry)..."
                        powershell """
                            Write-Output 'Verifying all pods are running...'
                            \$pods = kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app -o jsonpath='{.items[*].status.phase}'
                            
                            if (\$pods -match 'Running') {
                                Write-Output 'All pods are running successfully!'
                            } else {
                                Write-Output 'Some pods are not running. Current status:'
                                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app
                                kubectl describe pods -n ${KUBE_NAMESPACE} -l app=flask-app
                                exit 1
                            }
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo "[SUCCESS] Deployment completed!"
            powershell """
                Write-Output 'Final pod status:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app
                
                Write-Output ''
                Write-Output 'Service URL:'
                minikube service flask-service --url -n ${KUBE_NAMESPACE}
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
            powershell """
                Write-Output 'Debug information:'
                Write-Output '=================='
                Write-Output ''
                Write-Output 'Pod Status:'
                kubectl get pods -n ${KUBE_NAMESPACE}
                Write-Output ''
                Write-Output 'Pod Details:'
                kubectl describe pods -n ${KUBE_NAMESPACE} -l app=flask-app
                Write-Output ''
                Write-Output 'Pod Logs:'
                kubectl logs -n ${KUBE_NAMESPACE} -l app=flask-app --tail=50
                Write-Output ''
                Write-Output 'Images in Minikube:'
                & minikube -p minikube docker-env --shell powershell | Invoke-Expression
                docker images | Select-String ${IMAGE_NAME}
            """
        }
        always {
            echo "Pipeline execution completed at \${new Date()}"
        }
    }
}
