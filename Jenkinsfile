pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                # Install project dependencies from requirements.txt
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Application') {
            steps {
                script {
                    // Run Flask app in the background and save the process ID
                    sh "python3 main.py"
                }
            }
        }
    }
}
