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
                script {
                    def scriptOutput = sh(returnStdout: true, script: """
                            python ./update_os_py/main.py
                    """).trim()
                    env.SCRIPT_OUTPUT = scriptOutput
                    echo "Script output is ${env.SCRIPT_OUTPUT}"
                    if (!scriptOutput || !scriptOutput.size() || scriptOutput[0].toString().trim() == -1) {
                           error('Ошибка! Первый элемент массива равен -1.')
                    }
                }
            }
        }
      
        stage('Third') {
            steps {
                script {
                    def scriptOutput = sh(returnStdout: true, script: """
                            python ./update_os_py/second.py "${env.SCRIPT_OUTPUT}"
                    """).trim()
                    env.SCRIPT_OUTPUT = scriptOutput
                    echo "Script output is ${env.SCRIPT_OUTPUT}"
                }
            }
        }
    }
}
