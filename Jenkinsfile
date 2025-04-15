pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/kirviklife/upd_pg_ansible.git', branch: 'main'
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
