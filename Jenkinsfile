properties([
    parameters([
        choice(name: 'CHOICE_PARAMETER',
              choices: ['Option A', 'Option B'],
              description: 'Choose an option.'),
        choice(
            name: 'CONFIG_FILE',
            choices: [
                // Динамическая загрузка имен файлов из YAML
                loadYamlFilesFromWorkspace(),
            ],
            description: 'Choose the configuration file to be used.'
        )
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
                    def currentUser = env.BUILD_USER_ID ?: ""
                    echo "Текущий пользователь: ${currentUser}"
                    echo "Текущий пользователь: ${env.BUILD_USER_ID}"
                    timeout(time: 24, unit: 'HOURS') {
                        def userInput = input id: 'manual_approval', message: 'Требуется одобрение другим пользователем.', submitterParameter: 'APPROVER', submitter: "!${currentUser}"
                        env.userInput = userInput
                    }
                    if(env.userInput != currentUser){
                        error("Ошибка: нельзя согласовывать самому себе")
                    }
                    else{
                        echo "Согласовано пользователем: ${env.userInput}"
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
        stage('Read yml') {
            steps {
                script {
                    def workspacePath = pwd()
                    // Читаем файл filenames.yml, содержащий список остальных файлов
                    def files = readYaml(file: "${workspacePath}/vars/all.yml")
                    def contentsArray = [0,[]]
                    // Проходим по каждому файлу и читаем его содержимое
                    for (def filename : files.files) {
                        echo "Reading ${filename}"
                        
                        // Читаем каждый указанный файл и выводим его содержимое
                        def content = readYaml(file: "${workspacePath}/vars/${filename}")
                        contentsArray[1].add(content['parameter1'])
                        println(content)
                    }
                    println(contentsArray)
                    def jsonData = groovy.json.JsonOutput.toJson(contentsArray)
                    def scriptOutput = sh(returnStdout: true, script: """
                            python ./update_os_py/from_yml.py '${jsonData}'
                    """).trim()
                    env.SCRIPT_OUTPUT = scriptOutput
                    echo "Script output is ${env.SCRIPT_OUTPUT}"
                }
            }
        }
    }
}


// Функция для загрузки файлов из YAML
def loadYamlFilesFromWorkspace() {
    def workspacePath = "${env.JENKINS_HOME}/jobs/${JOB_NAME}/builds/${BUILD_NUMBER}/workspace/vars/all.yml"
    def yamlContent = readFile(workspacePath)
    return new groovy.json.JsonSlurperClassic().parseText(yamlContent)["files"] as List<String>
}