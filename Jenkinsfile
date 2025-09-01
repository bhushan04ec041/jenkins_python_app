pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/bhushan04ec041/jenkins_python_app"
        DOCKER_CREDS = "github-pat"
        GITHUB_CREDS = "github-pat"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'BR_bhushan',
                    credentialsId: "${GITHUB_CREDS}",
                    url: 'https://github.com/bhushan04ec041/jenkins_python_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push to GitHub Container Registry') {
            steps {
                script {
                    docker.withRegistry('https://ghcr.io', "${DOCKER_CREDS}") {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
        failure {
            echo "❌ Pipeline failed"
        }
        success {
            echo "✅ Image pushed to GHCR successfully"
        }
    }
}

