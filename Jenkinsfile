pipeline {
    agent any
    
    environment {
        // Define environment variables
        IMAGE_NAME = "python-learning-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = "docker.io" // Change to your registry URL (e.g., your-registry.com, gcr.io, etc.)
        DOCKER_REPO = "your-username/python-learning-app" // Change to your Docker Hub username or registry path
        DOCKER_CREDENTIALS_ID = "docker-hub-credentials" // Jenkins credential ID for Docker registry
    }
    
    stages {
        stage('Pull Repository') {
            steps {
                echo 'Stage 1: Pulling repository from remote...'
                // Clean workspace and checkout code
                cleanWs()
                checkout scm
                
                // Alternatively, you can specify a specific repository:
                // git branch: 'main', url: 'https://github.com/your-username/your-repo.git'
                
                echo 'Repository pulled successfully!'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Stage 2: Building Docker image...'
                script {
                    // Navigate to the directory containing Dockerfile and build the image
                    dir('python-learning') {
                        sh """
                            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        """
                    }
                }
                echo 'Docker image built successfully!'
            }
        }
        
        stage('Push Docker Image') {
            steps {
                echo 'Stage 3: Pushing Docker image to repository...'
                script {
                    // Login to Docker registry using Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", 
                                                    passwordVariable: 'DOCKER_PASSWORD', 
                                                    usernameVariable: 'DOCKER_USERNAME')]) {
                        sh """
                            # Login to Docker registry
                            echo \$DOCKER_PASSWORD | docker login ${DOCKER_REGISTRY} -u \$DOCKER_USERNAME --password-stdin
                            
                            # Tag images for registry
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG}
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${DOCKER_REPO}:latest
                            
                            # Push images to registry
                            docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG}
                            docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}:latest
                            
                            # Logout from registry
                            docker logout ${DOCKER_REGISTRY}
                        """
                    }
                }
                echo 'Docker image pushed successfully!'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
            // Clean up docker images if needed
            sh """
                # Remove old images (keep latest and current build)
                docker images ${IMAGE_NAME} --format "table {{.Tag}}" | grep -v -E "(latest|${IMAGE_TAG}|TAG)" | head -5 | xargs -r -I {} docker rmi ${IMAGE_NAME}:{} || true
            """
        }
        success {
            echo 'Pipeline succeeded! 🎉'
            echo "Docker image pushed to: ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG}"
            echo "Latest image available at: ${DOCKER_REGISTRY}/${DOCKER_REPO}:latest"
        }
        failure {
            echo 'Pipeline failed! ❌'
            // Cleanup local images on failure if needed
            sh """
                docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                docker rmi ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG} || true
                docker rmi ${DOCKER_REGISTRY}/${DOCKER_REPO}:latest || true
            """
        }
    }
}
