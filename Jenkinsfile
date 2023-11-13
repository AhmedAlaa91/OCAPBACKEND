pipeline {
     
       agent any
     
   stages {
    stage('build') {
      steps {
         sh 'python3 -m pip install django --break-system-packages'
         sh 'python3 -m venv .venv'
         sh '. .venv/bin/activate'
         sh 'python3 -m pip install poetry --break-system-packages'
         sh 'python3 -m poetry install '
         sh 'python3 -m pip install pytest --break-system-packages'
         sh 'python3 -m pip install pytest_django --break-system-packages'
         sh 'python3 -m pip install  pytest-cov --break-system-packages'
        
        
      }
    }
    stage('test') {
       steps {
        sh 'python3 -m pytest --reuse-db --cov=apps/website/views --cov-fail-under=30  tests'
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
      
