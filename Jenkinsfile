

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
        stage('Динамические параметры') {
            steps {
                script {
                    // Исходный массив файлов
                    def workspacePath = pwd()
                    // Читаем файл filenames.yml, содержащий список остальных файлов
                    def files_file = readYaml(file: "${workspacePath}/vars/all.yml")
                    def contentsArray = []
                    // Проходим по каждому файлу и читаем его содержимое
                    for (def filename : files_file.files) {
                        contentsArray.add(filename)
                    }
                    def files = contentsArray

                    // Генерируем динамический список параметров (чекбоксов)
                    def dynamicParams = [:]
                    files.each { file ->
                        dynamicParams.put(file, false) // Начальные значения - все false
                    }

                    // Запрашиваем у пользователя выбор параметров
                    def userInput = input message: 'Выберите файлы для включения',
                                          ok: 'Продолжить',
                                          parameters: dynamicParams.collect { key, value ->
                                              booleanParam(name: key, defaultValue: value)
                                          }

                    // Обрабатываем выбранные параметры
                    def vibor = []
                    files.each { file ->
                        if(userInput.get(file)) {
                            echo "- $file включен"
                            vibor.add("'${file}'")
                        } else {
                            echo "- $file выключен"
                        }
                    }
                    env.CLUSTER_CHECK = vibor
                }
            }
        }
        stage('Обработка выбранных файлов') {
            steps {
                script {
                    echo "Выбранные файлы для обработки: ${env.CLUSTER_CHECK}"
                }
            }
        }
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
                    def files = env.CLUSTER_CHECK.split(',')
                    def contentsArray = [0,[]]
                    // Проходим по каждому файлу и читаем его содержимое
                    for (def filename : files) {
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


