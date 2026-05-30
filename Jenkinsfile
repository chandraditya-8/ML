pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t nutripredict .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat '''
                docker stop nutripredict-container
                docker rm nutripredict-container
                exit /b 0
                '''
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d --name nutripredict-container -p 5000:5000 nutripredict'
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