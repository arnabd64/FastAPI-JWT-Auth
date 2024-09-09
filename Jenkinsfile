pipeline {
    agent any
    stages {
        stage ("dependency") {
            sh "pip install -r requirements.txt"
        }

        stage ("build") {
            echo "build-stage"
            sh "python3 main.py"
        }
    }
}