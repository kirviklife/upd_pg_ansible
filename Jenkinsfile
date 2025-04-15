pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'git_sign_ssh', url: 'https://github.com/kirviklife/upd_pg_ansible.git'
            }
        }

        stage('Deploy Playbook') {
            steps {
                ansiblePlaybook credentialsId: 'git_sign_ssh', disableHostKeyChecking: true, installation: 'Ansible', inventory: 'hosts', playbook: 'playbooks/test_playbook.yml'
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
