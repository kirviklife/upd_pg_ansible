properties([
    parameters([
        choice(name: 'CHOICE_PARAMETER',
              choices: ['Option A', 'Option B'],
              description: 'Choose an option.')
    ])
])

pipeline {
    agent any
    parameters {
        string(name: 'BUILD_TYPE', defaultValue: '', description: 'Тип сборки')
    }
    
    stages {
        
        stage('Wait for Approval') {
            steps {
                script {
                    def cause = currentBuild.getBuildCauses('hudson.model.Cause$UserIdCause')
                    echo "userName: ${cause.userName[0]}"
                    timeout(time: 24, unit: 'HOURS') {
                        input id: 'manual_approval', message: 'Требуется одобрение другим пользователем.', submitter: "!${cause.userName}"
                    }
                    echo "Текущий пользователь: ${currentUser}"
                }
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'git_sign_ssh', url: 'https://github.com/kirviklife/upd_pg_ansible.git'
            }
        }

        stage('Deploy Playbook') {
            when {
                allOf {
                    equals expected: params.BUILD_TYPE, actual: 'debug'
                    equals expected: params.CHOICE_PARAMETER, actual: 'Option A'
                }
            }
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
                    def parsedArray = readJSON text: scriptOutput
                    // Проверяем первый элемент массива
                    if(parsedArray.getAt(0) == -1){
                        error("Ошибка: первый элемент массива равен -1")
                        echo "Первый элемент массива: ${parsedArray.getAt(1)}"
                    }else{
                        env.SCRIPT_OUTPUT = scriptOutput
                        echo "Первый элемент массива: ${parsedArray.getAt(0)}"
                        echo "Script output is ${env.SCRIPT_OUTPUT}"
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
