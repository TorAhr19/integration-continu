pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonar-token')
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage('Installation des dependances') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Linting') {
            steps {
                sh '''
                    . venv/bin/activate
                    pylint app/ --output-format=text --fail-under=5.0 || true
                '''
            }
        }

        stage('Tests et couverture') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing \
                        --junitxml=test-results.xml \
                        -v
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Verification couverture >= 80%') {
            steps {
                sh '''
                    . venv/bin/activate
                    coverage report --fail-under=80
                '''
            }
        }

        stage('Complexite Radon') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "=== Complexite cyclomatique ==="
                    radon cc app/ -s -a
                    echo ""
                    echo "=== Indice de maintenabilite ==="
                    radon mi app/ -s
                '''
            }
        }

        stage('Analyse SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminee.'
        }
        success {
            echo 'Build reussi - tous les criteres qualite sont satisfaits.'
        }
        failure {
            echo 'Build echoue - verifier les logs ci-dessus.'
        }
    }
}
