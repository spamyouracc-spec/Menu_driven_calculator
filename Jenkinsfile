pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'santhiya1907'
        IMAGE_NAME = '24MIS0405'
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat 'python -m venv .venv'
                bat '.venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '.venv\\Scripts\\pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    bat 'copy "%KUBECONFIG_FILE%" "%WORKSPACE%\\kubeconfig"'
                    bat 'set KUBECONFIG=%WORKSPACE%\\kubeconfig && kubectl set image deployment/calculator-deployment calculator=%DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%'
                    bat 'set KUBECONFIG=%WORKSPACE%\\kubeconfig && kubectl rollout status deployment/calculator-deployment'
                    bat 'set KUBECONFIG=%WORKSPACE%\\kubeconfig && kubectl get svc calculator-service'
                }
            }
        }
    }
}