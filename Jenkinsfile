pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t barber-app:latest .'
            }
        }

        stage('Start MongoDB') {
            steps {
                sh '''
                    docker stop mongodb-test || true
                    docker rm mongodb-test || true
                    docker run -d --name mongodb-test \
                        -p 27017:27017 \
                        -e MONGO_INITDB_ROOT_USERNAME=admin \
                        -e MONGO_INITDB_ROOT_PASSWORD=pass \
                        -e MONGO_INITDB_DATABASE=barber_shop \
                        mongo:8.0.4
                    sleep 15
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker stop barber-app || true
                    docker rm barber-app || true
                    docker run -d --name barber-app \
                        -p 5000:5000 \
                        --add-host host.docker.internal:host-gateway \
                        -e MONGO_HOST=host.docker.internal \
                        -e MONGO_USER=admin \
                        -e MONGO_PASS=pass \
                        -e MONGO_DB=barber_shop \
                        barber-app:latest
                    sleep 10
                '''
            }
        }

        stage('Debug - Show Logs') {
            steps {
                sh '''
                    echo "===== BARBER APP LOGS ====="
                    docker logs barber-app || echo "Container not running!"
                    echo ""
                    echo "===== CONTAINER STATUS ====="
                    docker ps -a
                    echo ""
                    echo "===== HEALTH CHECK ====="
                    curl -f http://localhost:5000/health || echo "Health check failed!"
                '''
            }
        }

        stage('Test Endpoint') {
            steps {
                sh 'curl -f http://localhost:5000/ || exit 1'
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    docker stop barber-app mongodb-test || true
                    docker rm barber-app mongodb-test || true
                '''
            }
        }
    }
}