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
        stage('Verify Minikube') {
            steps {
                script {
                    echo "Checking Minikube status..."
                    powershell """
                        \$status = minikube status --format='{{.Host}}' 2>&1
                        if (\$status -notmatch 'Running') {
                            Write-Output 'Starting Minikube...'
                            minikube start
                            Start-Sleep -Seconds 10
                        } else {
                            Write-Output 'Minikube is already running'
                        }
                        minikube status
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
                        kubectl set image deployment/flask-k8s-deployment flask-k8s-app=${IMAGE_NAME}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                        kubectl patch deployment flask-k8s-deployment -n ${KUBE_NAMESPACE} -p '{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"flask-k8s-app\",\"imagePullPolicy\":\"Never\"}]}}}}'
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
                        kubectl rollout status deployment/flask-k8s-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                        
                        Write-Output 'Current pods:'
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app -o wide
                        
                        Write-Output 'Current services:'
                        kubectl get svc -n ${KUBE_NAMESPACE}
                        
                        Write-Output 'Getting service URL...'
                        minikube service flask-k8s-service --url -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished at ${new Date()}"
            powershell """
                Write-Output 'Attempting to get application logs...'
                \$pods = kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app -o jsonpath='{.items[0].metadata.name}' 2>&1
                if (\$LASTEXITCODE -eq 0 -and \$pods) {
                    kubectl logs \$pods -n ${KUBE_NAMESPACE} --tail=50
                } else {
                    Write-Output 'No pods available yet'
                }
            """
        }
        success {
            echo "[SUCCESS] Deployment successful!"
            powershell """
                Write-Output '=================================='
                Write-Output 'Final Deployment Status:'
                kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app -o wide
                kubectl get svc -n ${KUBE_NAMESPACE}
                Write-Output '=================================='
                Write-Output 'Access your application at:'
                minikube service flask-k8s-service --url -n ${KUBE_NAMESPACE}
                Write-Output '=================================='
            """
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
            powershell """
                Write-Output 'Minikube Status:'
                minikube status
                
                Write-Output ''
                Write-Output 'Recent Events:'
                kubectl get events -n ${KUBE_NAMESPACE} --sort-by=.lastTimestamp | Select-Object -Last 15
                
                Write-Output ''
                Write-Output 'All Pods:'
                kubectl get pods -n ${KUBE_NAMESPACE} -o wide
                
                Write-Output ''
                Write-Output 'Pod Details (if any):'
                \$pods = kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app -o jsonpath='{.items[*].metadata.name}' 2>&1
                if (\$pods) {
                    foreach (\$pod in \$pods.Split()) {
                        Write-Output "Describing pod: \$pod"
                        kubectl describe pod \$pod -n ${KUBE_NAMESPACE}
                    }
                }
            """
        }
    }
}