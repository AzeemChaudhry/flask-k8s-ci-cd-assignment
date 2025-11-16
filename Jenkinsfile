// Jenkinsfile for CI/CD pipeline
// This pipeline builds a Docker image, deploys to Kubernetes, and verifies deployment

pipeline {
    agent any  // Run on any available Jenkins agent

    environment {
        // Name of the Docker image
        IMAGE_NAME = "flask-k8s-app"
        // Kubernetes namespace to deploy to
        KUBE_NAMESPACE = "default"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:latest..."
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Applying Kubernetes manifests..."
                    // Apply all manifests in kubernetes/ folder
                    sh "kubectl apply -f kubernetes/"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    echo "Checking rollout status..."
                    // Wait for deployment to finish rolling out
                    sh "kubectl rollout status deployment/flask-k8s-deployment"
                    
                    echo "Listing pods and services..."
                    sh "kubectl get pods -n ${KUBE_NAMESPACE}"
                    sh "kubectl get svc -n ${KUBE_NAMESPACE}"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Check logs for details."
        }
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Pipeline failed. Please investigate."
        }
    }
}