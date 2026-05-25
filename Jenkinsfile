pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'YOUR_GITHUB_REPO'
            }
        }

        stage('Build Docker') {
            steps {
                bat 'docker build -t nutripredict .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 5000:5000 nutripredict'
            }
        }
    }
}