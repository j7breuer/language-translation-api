pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                echo '\n=======================\n[START] Initializing...\n=======================\n'
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL} \n"
                echo "Installing PyTorch..."
                sh 'pip3.9 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu'
                echo "Installing requirements.txt"
                sh 'pip3.9 install -r requirements.txt'
                echo '\n=====================\n[END] Initializing...\n=====================\n'
            }
        }
        stage('PyTest Unit Tests') {
            steps {
                echo '\n============================\n[START] PyTest Unit Tests...\n============================\n'
                echo 'Running pytest...'
                #sh 'python3.9 -m pytest --cov . --cov-report xml'
                echo '\n==========================\n[END] PyTest Unit Tests...\n==========================\n'
            }
        }
        stage('Sonar Scans') {
            environment {
                scannerHome = tool 'SonarQubeScanner-4.7.0'
            }
            steps {
                withSonarQubeEnv('SonarQube-8.3.1') {
                    echo '\n============================\n[START] Sonar Scans...\n============================\n'
                    sh '/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner-4.7.0/bin/sonar-scanner'
                    echo '\n============================\n[END] Sonar Scans...\n============================\n'
                }
            }
        }
        stage('Docker Build') {
            steps {
                echo '\n=======================\n[START] Docker Build...\n=======================\n'
                echo 'Running docker build...'
                echo '\n=====================\n[END] Docker Build...\n=====================\n'
            }
        }
        stage('Docker Publish') {
            steps {
                echo '\n===========================\n[START] Publishing Build...\n===========================\n'
                echo 'Running docker push...'
                echo '\n=========================\n[END] Publishing Build...\n=========================\n'
            }
        }
        stage('Environment Cleanup') {
            steps {
                echo '\n==============================\n[START] Cleanup and Removal...\n==============================\n'
                echo 'Running docker rm...'
                echo '\n============================\n[END] Cleanup and Removal...\n============================\n'
            }
        }
    }
}