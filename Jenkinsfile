pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        BACKEND_IMAGE = "uniguard-backend:${BUILD_NUMBER}"
        FRONTEND_IMAGE = "uniguard-frontend:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Backend') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r backend/requirements.txt
                    python -m py_compile backend/main.py
                '''
            }
        }

        stage('Validate Frontend') {
            steps {
                sh '''
                    cd frontend
                    npm ci
                    npm run build
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t "$BACKEND_IMAGE" backend
                    docker build -t "$FRONTEND_IMAGE" frontend
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    docker compose up -d --build
                    curl -f http://localhost:8000/health
                    curl -f http://localhost:3000
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose up -d --build'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}