pipeline {
     
     agent any 
     
   stages {
    stage('build') {
      steps {

         sh 'python3 -m venv .venv'
         sh 'source .\\.venv\\bin\\activate'
         sh 'python3 -m pip install poetry'
         sh 'python3 -m poetry install '
         sh 'python3 -m pip install pytest'
         sh 'python3 -Xutf8 manage.py loaddata data_dumped.json'
        
      }
    }
    stage('test') {
       steps {
        sh 'python3 -m pytest --reuse-db --cov=apps\\website\\views --cov-fail-under=30 --junitxml=test-reports/report.xml tests'
          sh' python3 -m coverage xml'
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
      
