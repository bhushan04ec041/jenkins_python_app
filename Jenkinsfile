pipeline {
    agent any

    triggers {
        githubPush()   // Automatically triggered by GitHub webhook
    }

    environment {
        IMAGE_NAME = "bhushan04ec041/jenkins_python_app"
        IMAGE_TAG  = "${BUILD_NUMBER}"   // unique tag per build
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'BR_bhushan',
                    url: 'https://github.com/bhushan04ec041/jenkins_python_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  echo "Building Docker image..."
                  docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh '''
                      echo "Logging into DockerHub..."
                      echo $DOCKER_TOKEN | docker login -u bhushan04ec041 --password-stdin
                      echo "Pushing image to DockerHub..."
                      docker push $IMAGE_NAME:$IMAGE_TAG
                      echo "Tagging latest..."
                      docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                      docker push $IMAGE_NAME:latest
                    '''
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
