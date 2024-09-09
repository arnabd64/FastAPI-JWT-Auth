pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                # Build the Docker image
                docker compose up --build -d
                '''
            }
        }
    }
}
