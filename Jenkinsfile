pipeline {
    agent any
    
    environment {
        // Define environment variables
        IMAGE_NAME = "python-learning-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = "docker.io" // Change to your registry URL (e.g., your-registry.com, gcr.io, etc.)
        DOCKER_REPO = "wahajaziz/python-learning-app" // Change to your Docker Hub username or registry path
        // Docker registry auth via Personal Access Token (PAT)
        DOCKER_USERNAME = "wahajaziz" // Jenkinsfile-readable username; keep secret parts only in Jenkins credentials store
        DOCKER_PAT_CREDENTIALS_ID = "docker-hub-pat" // Jenkins Secret Text credential ID that stores the PAT

        // Git (private repo) configuration
        GIT_REPO_URL = "git@github.com:WahajAziz/python-learning.git" // Replace with your repo URL
        GIT_BRANCH = "main" // Replace with your branch
        GIT_CREDENTIALS_ID = "git-repo-credentials" // Jenkins credential ID for your Git repo (username/password or SSH key)

        // Paths for Docker build (explicit to avoid path issues)
        DOCKERFILE_PATH = "python-learning/Dockerfile"
        DOCKER_BUILD_CONTEXT = "python-learning"
    }
    
    stages {
        stage('Pull Repository') {
            steps {
                echo 'Stage 1: Pulling repository from remote...'
                // Clean workspace and checkout code
                cleanWs()
                // Explicit checkout using credentials for private repositories
                git branch: "${GIT_BRANCH}", credentialsId: "${GIT_CREDENTIALS_ID}", url: "${GIT_REPO_URL}"

                echo 'Repository pulled successfully!'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Stage 2: Building Docker image...'
                script {
                    // Build image using explicit dockerfile and context paths from workspace root
                    sh """
                        ls -la
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    """
                }
                echo 'Docker image built successfully!'
            }
        }
        
        stage('Push Docker Image') {
            steps {
                echo 'Stage 3: Pushing Docker image to repository...'
                script {
                    // Login to Docker registry using a Personal Access Token (PAT)
                    withCredentials([string(credentialsId: "${DOCKER_PAT_CREDENTIALS_ID}", variable: 'DOCKER_PAT')]) {
                        sh """
                            # Login to Docker registry
                            echo \$DOCKER_PAT | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USERNAME} --password-stdin
                            
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
