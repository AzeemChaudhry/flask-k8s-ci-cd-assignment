// Jenkinsfile for CI/CD pipeline with Minikube
// This pipeline builds a Docker image, deploys to Kubernetes, and verifies deployment
pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "flask-k8s-app"
        IMAGE_TAG = "${BUILD_NUMBER}"  // Use build number for versioning
        KUBE_NAMESPACE = "default"
        DOCKER_BUILDKIT = "1"  // Enable BuildKit for better caching
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code..."
                    checkout scm
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                    
                    // For minikube: Use minikube's Docker daemon
                    sh '''
                        # Point to minikube's Docker daemon
                        eval $(minikube -p minikube docker-env)
                        
                        # Build image inside minikube
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        
                        # Verify image was built
                        docker images | grep ${IMAGE_NAME}
                    '''
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    echo "Updating image tag in Kubernetes manifests..."
                    
                    // Update deployment to use the new image tag
                    sh """
                        sed -i 's|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g' kubernetes/deployment.yaml
                        
                        # Also ensure imagePullPolicy is set correctly for local images
                        if ! grep -q "imagePullPolicy: Never" kubernetes/deployment.yaml; then
                            sed -i '/image: ${IMAGE_NAME}:/a\\        imagePullPolicy: Never' kubernetes/deployment.yaml
                        fi
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Applying Kubernetes manifests..."
                    
                    sh """
                        # Apply all manifests
                        kubectl apply -f kubernetes/ -n ${KUBE_NAMESPACE}
                        
                        # Force a rollout restart to pick up new image
                        kubectl rollout restart deployment/flask-k8s-deployment -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Waiting for deployment to be ready..."
                    
                    sh """
                        # Wait for rollout to complete (timeout after 5 minutes)
                        kubectl rollout status deployment/flask-k8s-deployment -n ${KUBE_NAMESPACE} --timeout=5m
                        
                        echo "=== Pods ==="
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-k8s-app
                        
                        echo "=== Services ==="
                        kubectl get svc -n ${KUBE_NAMESPACE}
                        
                        echo "=== Deployment Details ==="
                        kubectl describe deployment flask-k8s-deployment -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "Performing health check..."
                    
                    sh """
                        # Get the service URL
                        minikube service flask-k8s-service --url -n ${KUBE_NAMESPACE} || true
                        
                        # Try to curl the service (optional)
                        SERVICE_URL=\$(minikube service flask-k8s-service --url -n ${KUBE_NAMESPACE} 2>/dev/null || echo "")
                        if [ -n "\$SERVICE_URL" ]; then
                            echo "Testing service at: \$SERVICE_URL"
                            curl -f \$SERVICE_URL || echo "Health check failed, but continuing..."
                        fi
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished at ${new Date()}"
            
            // Print pod logs for debugging if something failed
            script {
                sh """
                    echo "=== Recent Pod Logs ==="
                    kubectl logs -l app=flask-k8s-app -n ${KUBE_NAMESPACE} --tail=50 || true
                """ 
            }
        }
        success {
            echo "✅ Deployment successful!"
            echo "Access your application using: minikube service flask-k8s-service -n ${KUBE_NAMESPACE}"
        }
        failure {
            echo "❌ Pipeline failed. Check the logs above for details."
            
            script {
                sh """
                    echo "=== Debugging Information ==="
                    kubectl get events -n ${KUBE_NAMESPACE} --sort-by='.lastTimestamp' | tail -20
                    kubectl get pods -n ${KUBE_NAMESPACE} -o wide
                """ 
            }
        }
    }
}
