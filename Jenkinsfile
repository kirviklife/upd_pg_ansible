pipeline {
    agent {
        node {
            label 'TestNode' 
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
