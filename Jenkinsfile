properties([
    parameters([
        choice(name: 'CHOICE_PARAMETER',
              choices: ['Option A', 'Option B'],
              description: 'Choose an option.')
    ])
])
options {
  withBuildUser()
}
pipeline {
    agent any
    parameters {
        string(name: 'BUILD_TYPE', defaultValue: '', description: 'Тип сборки')
    }
    
    stages {
        
        stage('Подтверждение') {
            steps {
                script {
                    def currentUser = env.BUILD_USER_ID ?: env.USERNAME // Получаем ID текущего пользователя
                    echo "${currentUser}"
                    input message: 'Требуется одобрение',
                          parameters: [
                              choice(name: 'approve', choices: ['Да', 'Нет'], description: 'Выберите Да, чтобы продолжить'),
                              string(name: 'confirmationUser', defaultValue: '', description: 'Укажите имя пользователя, подтверждающего действие')
                          ],
                          submitterParameter: 'submitter',
                          ok: 'Продолжить'  
                }
                
                script {
                    if ("${params.submitter}" != "${currentUser}") { // Проверяем, подтвердил ли другой пользователь
                        echo "Действие подтверждено пользователем ${params.submitter}"
                    } else {
                        error("Операция должна быть подтверждена другим пользователем")
                    }
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
