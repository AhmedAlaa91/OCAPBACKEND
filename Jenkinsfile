pipeline {
     
     agent any 
     
   stages {
    stage('build') {
      steps {

         bat 'pip install poetry'
          bat 'poetry install --sync'
      }
    }
    stage('test') {
       steps {
        bat 'python -m pytest --reuse-db --cov=apps\\website\\views --cov-fail-under=30 --junitxml=test-reports/report.xml tests'
          bat' python -m coverage xml'
      }  
       post {
        always {
          junit 'test-reports/*.xml'
         step([$class: 'CoberturaPublisher', coberturaReportFile: 'coverage.xml'])
        }
      }    
    }
  }
}
      
