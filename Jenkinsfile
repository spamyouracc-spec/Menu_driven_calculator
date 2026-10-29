pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'yourdockerhubusername'
        IMAGE_NAME = 'calculator'
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/<your-username>/calculator-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. .venv/bin/activate && pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    sh 'cp $KUBECONFIG_FILE $WORKSPACE/kubeconfig'
                    sh 'export KUBECONFIG=$WORKSPACE/kubeconfig'
                    sh 'kubectl set image deployment/calculator-deployment calculator=${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}'
                    sh 'kubectl rollout status deployment/calculator-deployment'
                    sh 'kubectl get svc calculator-service'
                }
            }
        }
    }
}