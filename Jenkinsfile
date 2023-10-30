pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('poetry') {
      steps {
        bat 'pip install poetry'
      }
    }
    stage('build') {
      steps {
        bat 'poetry install'
      }
    }
    stage('test') {
      steps {
        bat 'python test.py'
      }  
    }
  }
}