pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t nutripredict .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop nutripredict-container || true'
                sh 'docker rm nutripredict-container || true'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d --name nutripredict-container -p 5000:5000 nutripredict'
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}