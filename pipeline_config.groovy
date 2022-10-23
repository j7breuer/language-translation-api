pipeline {
    agent any

    stages {
        stage('Init') {
            steps {
                echo 'Initializing...'
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
            }
        }
        stage('Unit Testing') {
            steps {
                echo 'Testing...'
                echo 'Running pytest...'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                echo 'Running docker build...'
            }
        }
        stage('Publish') {
            steps {
                echo 'Publishing...'
                echo 'Running docker push...'
            }
        }
        stage('SonarQube Code Analysis') {
            steps {
                echo 'Cleaning...'
                echo 'Running docker rm...'
            }
        }
    }
}