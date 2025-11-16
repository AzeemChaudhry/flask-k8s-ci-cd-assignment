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
                        \$result1 = minikube image load ${IMAGE_NAME}:${IMAGE_TAG} 2>&1
                        Write-Output \$result1
                        
                        Write-Output ''
                        Write-Output 'Loading image ${IMAGE_NAME}:latest into Minikube...'
                        \$result2 = minikube image load ${IMAGE_NAME}:latest 2>&1
                        Write-Output \$result2
                        
                        Write-Output ''
                        Write-Output 'Waiting for images to be available...'
                        Start-Sleep -Seconds 5
                        
                        Write-Output ''
                        Write-Output 'Verifying images are in minikube registry...'
                        \$images = minikube image ls 2>&1 | Select-String '${IMAGE_NAME}'
                        
                        if (\$images) {
                            Write-Output 'Found images:'
                            Write-Output \$images
                        } else {
                            Write-Error 'ERROR: Images not found in minikube registry!'
                            Write-Output 'Attempting to list all images in minikube:'
                            minikube image ls
                            exit 1
                        }
                        
                        Write-Output ''
                        Write-Output 'Images loaded and verified successfully!'
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
