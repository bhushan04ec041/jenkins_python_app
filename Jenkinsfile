pipeline {
    agent any

    environment {
        IMAGE_NAME = "bhushan04ec041/jenkins_python_app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo "🛠 Building Docker image $IMAGE_NAME:$IMAGE_TAG..."
                sh "docker build -t $IMAGE_NAME:$IMAGE_TAG ."
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "🚀 Logging in and pushing Docker image..."
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker push $IMAGE_NAME:$IMAGE_TAG
                        docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                        docker push $IMAGE_NAME:latest
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI pipeline successful. Triggering CD pipeline..."
            build job: 'python_app_CD', wait: false
        }
        failure {
            echo "❌ CI pipeline failed."
        }
    }
}

