pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "bhushan04ec041/jenkins_python_app"
        COMPOSE_FILE = "docker-compose.yml"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'BR_bhushan', url: 'https://github.com/your_repo.git'
            }
        }

        stage('Get Latest Docker Image Tag') {
            steps {
                script {
                    def response = sh(
                        script: "curl -s https://registry.hub.docker.com/v2/repositories/${DOCKER_IMAGE}/tags?page_size=1",
                        returnStdout: true
                    ).trim()
                    // Parse JSON to get tag (using groovy JsonSlurper)
                    def json = new groovy.json.JsonSlurper().parseText(response)
                    env.LATEST_TAG = json.results[0].name
                    echo "Latest Docker image tag: ${env.LATEST_TAG}"
                }
            }
        }

        stage('Update docker-compose.yml') {
            steps {
                script {
                    echo "Updating docker-compose.yml with tag: ${env.LATEST_TAG}"
                    sh """
                    sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${LATEST_TAG}|' ${COMPOSE_FILE}
                    """
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh """
                docker-compose -f ${COMPOSE_FILE} down
                docker-compose -f ${COMPOSE_FILE} up -d
                """
            }
        }
    }

    post {
        failure {
            echo "Deployment failed!"
        }
        success {
            echo "Deployment completed successfully!"
        }
    }
} 
