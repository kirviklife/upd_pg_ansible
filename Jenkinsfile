pipeline {
    agent {
     node {
      label '192.168.56.102' 
   }
}
    stages {
        stage('First') {
            steps {
                echo 'Hello World'
            }
        }
      
        stage('Second') {
            steps {
                echo 'This is Demo of Jenkins Pipeline Script from SCM'
            }
        }
      
        stage('Third') {
            steps {
                echo 'Last stage : blogoncode.com'
            }
        }
    }
}
