pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: 'https://github.com/oscarnnede/oscar-pro.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t barber-app:latest .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                    docker stop barber-app || true
                    docker rm barber-app || true
                    docker run -d --name barber-app -p 5000:5000 barber-app:latest
                '''
            }
        }

        stage('Test Endpoint') {
            steps {
                sh '''
                    sleep 5
                    curl -f http://localhost:5000/ || exit 1
                '''
            }
        }
    }
}