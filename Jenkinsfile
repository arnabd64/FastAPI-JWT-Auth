pipeline {
    agent any
    stages {
        stage ("dependency") {
            step {
                sh "pip install -r requirements.txt"
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
