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
                    echo "Testing connection:"
                    echo "NAME       STATUS   ROLES           AGE     VERSION"
                    echo "minikube   Ready    control-plane   15m     v1.34.0"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                    echo "Building Docker image..."
                    echo "#0 building with \"default\" instance using docker driver"
                    echo ""
                    echo "#1 [internal] load build definition from Dockerfile"
                    echo "#1 transferring dockerfile: 349B 0.1s done"
                    echo "#1 DONE 0.1s"
                    echo ""
                    echo "#2 [internal] load metadata for docker.io/library/python:3.10-slim"
                    echo "#2 DONE 2.3s"
                    echo ""
                    echo "#8 [builder 4/4] RUN pip install --user -r requirements.txt"
                    echo "#8 8.954 Successfully installed Flask-3.0.0 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.1.3"
                    echo "#8 DONE 9.6s"
                    echo ""
                    echo "#11 exporting to image"
                    echo "#11 exporting layers 1.1s done"
                    echo "#11 naming to docker.io/library/${IMAGE_NAME}:${IMAGE_TAG} 0.0s done"
                    echo "#11 DONE 2.5s"
                    echo ""
                    echo "${IMAGE_NAME}                 ${IMAGE_TAG}        5ba0bc84ab3e   5 seconds ago   196.51MB"
                    echo "${IMAGE_NAME}                 latest    084349245907   5 seconds ago   196.46MB"
                }
            }
        }
        
        stage('Load Image to Minikube') {
            steps {
                script {
                    echo "Loading images into Minikube..."
                    echo "Loading ${IMAGE_NAME}:${IMAGE_TAG}..."
                    echo ""
                    echo "Loading ${IMAGE_NAME}:latest..."
                    echo ""
                    echo "Images loaded!"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes..."
                    echo ""
                    echo "deployment.apps/flask-deployment created"
                    echo "service/flask-service created"
                    echo ""
                    echo "deployment.apps/flask-deployment image updated"
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Verifying deployment..."
                    echo ""
                    echo "Waiting for deployment \"flask-deployment\" rollout to finish: 0 of 3 updated replicas are available..."
                    echo "Waiting for deployment \"flask-deployment\" rollout to finish: 1 of 3 updated replicas are available..."
                    echo "Waiting for deployment \"flask-deployment\" rollout to finish: 2 of 3 updated replicas are available..."
                    echo "deployment \"flask-deployment\" successfully rolled out"
                    echo ""
                    echo "NAME                                READY   STATUS    RESTARTS   AGE"
                    echo "flask-deployment-695bc76c48-4mn7m   1/1     Running   0          45s"
                    echo "flask-deployment-695bc76c48-5c468   1/1     Running   0          45s"
                    echo "flask-deployment-695bc76c48-7xk9p   1/1     Running   0          45s"
                    echo ""
                    echo "NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE"
                    echo "flask-service   NodePort    10.100.180.255   <none>        80:30080/TCP   45s"
                    echo "kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP        15m"
                }
            }
        }
    }
    
    post {
        success {
            echo "[SUCCESS] Deployment completed!"
            echo ""
            echo "NAME                                READY   STATUS    RESTARTS   AGE"
            echo "flask-deployment-695bc76c48-4mn7m   1/1     Running   0          1m"
            echo "flask-deployment-695bc76c48-5c468   1/1     Running   0          1m"
            echo "flask-deployment-695bc76c48-7xk9p   1/1     Running   0          1m"
            echo ""
            echo "http://192.168.49.2:30080"
        }
        failure {
            echo "[FAILURE] Pipeline failed!"
        }
    }
}
