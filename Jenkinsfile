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
                ansiblePlaybook credentialsId: 'SSH', disableHostKeyChecking: true, installation: 'Ansible', inventory: 'hosts', playbook: 'playbooks/test_playbook.yml'
            }
        }        
      
        stage('Second') {
            steps {
                def scriptOutput = sh(returnStdout: true, script: """
                        python ./update_os_py/main.py '[0]' && echo "Success" || exit 1
                """).trim()
                env.SCRIPT_OUTPUT = scriptOutput
                echo "Script output is ${env.SCRIPT_OUTPUT}"
            }
        }
      
        stage('Third') {
            steps {
                echo 'Last stage : blogoncode.com'
            }
        }
    }
}
