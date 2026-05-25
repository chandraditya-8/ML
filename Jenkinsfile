pipeline {

    agent any

    stages {

        stage('Clone Repo') {

            steps {

                git 'https://github.com/chandraditya-8/ML.git'

            }

        }

        stage('Build Docker Image') {

            steps {

                bat 'docker build -t nutripredict .'

            }

        }

        stage('Stop Old Container') {

            steps {

                bat 'docker stop nutripredict-container || exit 0'
                bat 'docker rm nutripredict-container || exit 0'

            }

        }

        stage('Run Container') {

            steps {

                bat 'docker run -d --name nutripredict-container -p 5000:5000 nutripredict'

            }

        }

    }

}