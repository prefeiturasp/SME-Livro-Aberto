pipeline {
    agent {
      node { 
        label 'py-uniformes'
      }
    }
    
    options {
      buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
      disableConcurrentBuilds()
      skipDefaultCheckout()  
    }
    
        
  stages {
    stage('CheckOut') {
        steps {
          
          checkout scm

        }
      }
      
    stage('Analise Codigo') {
          when {
            branch 'homolog'
          }
            steps {
                sh 'sonar-scanner \
                    -Dsonar.projectKey=SME-Livro-Aberto \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonar.sme.prefeitura.sp.gov.br \
                    -Dsonar.login=fa261ec309c7cfeb7c8474ee1f1daa9094de327d'
                              }
       }
         
    stage('Docker build DEV') {
        when {
          branch 'develop'
        }
          steps {
          // Start JOB Rundeck para build das imagens Docker
      
          script {
           step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
                               
              //JOB DE BUILD
              jobId: "ae44872a-882d-4a79-b3a2-1ff44bdcbb3a",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
           }
        }
      }

    stage('Deploy DEV') {
        when {
          branch 'develop'
        }
          steps {
            //Start JOB Rundeck para update de deploy Kubernetes DEV
         
            script {
                step([$class: "RundeckNotifier",
                  includeRundeckLogs: true,
                  jobId: "674c4ff4-c572-4e1b-a620-00003555bb52",
                  nodeFilters: "",
                  //options: """
                  //     PARAM_1=value1
                  //    PARAM_2=value2
                  //     PARAM_3=
                  //     """,
                  rundeckInstance: "Rundeck-SME",
                  shouldFailTheBuild: true,
                  shouldWaitForRundeckJob: true,
                  tags: "",
                  tailLog: true])
              }
          }
      }
		
	  stage('Docker build HOM') {
            when {
                branch 'homolog'
            }
            steps {
              // Start build das imagens Docker
      
          script {
            step([$class: "RundeckNotifier",
                includeRundeckLogs: true,
                    
                
                //JOB DE BUILD
                jobId: "a7aba119-30d4-459a-a9c9-71da83d7365d",
                nodeFilters: "",
                //options: """
                //     PARAM_1=value1
                //    PARAM_2=value2
                //     PARAM_3=
                //     """,
                rundeckInstance: "Rundeck-SME",
                shouldFailTheBuild: true,
                shouldWaitForRundeckJob: true,
                tags: "",
                tailLog: true])
           }
          }
        }    
       
    stage('Deploy HOM') {
          when {
            branch 'homolog'
          }
          steps {
            
            timeout(time: 24, unit: "HOURS") {
               telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
               input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'bruno_buzzo, calvin_rossinhole, kelwy_oliveira'
            }
            //Start JOB Rundeck para update de imagens no host homologação 
         
            script {
                step([$class: "RundeckNotifier",
                includeRundeckLogs: true,
                jobId: "7945f869-fe18-4901-8d4a-5d4c08eee02c",
                nodeFilters: "",
                //options: """
                //     PARAM_1=value1
                //    PARAM_2=value2
                //     PARAM_3=
                //     """,
                rundeckInstance: "Rundeck-SME",
                shouldFailTheBuild: true,
                shouldWaitForRundeckJob: true,
                tags: "",
                tailLog: true])
            }
         }
        }
	    
	  stage('Docker build PROD') {
        when {
          branch 'master'
        }
        steps {
            
            // Start JOB Rundeck para build das imagens Docker
      
            script {
              step([$class: "RundeckNotifier",
                includeRundeckLogs: true,
                
                
                //JOB DE BUILD
                jobId: "36670f2b-8851-454d-bae7-417209cbe5f5",
                nodeFilters: "",
                //options: """
                //     PARAM_1=value1
                //    PARAM_2=value2
                //     PARAM_3=
                //     """,
                rundeckInstance: "Rundeck-SME",
                shouldFailTheBuild: true,
                shouldWaitForRundeckJob: true,
                tags: "",
                tailLog: true])
            }
         }
      }           
    
    stage('Deploy PROD') {
            when {
                branch 'master'
            }
            steps {
                timeout(time: 24, unit: "HOURS") {
                telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
                input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'bruno_buzzo, calvin_rossinhole, kelwy_oliveira'
                }
                    
            
                script {
                    step([$class: "RundeckNotifier",
                    includeRundeckLogs: true,
                    jobId: "8332c80b-5793-437e-afcb-b32bf3e28a1f",
                    nodeFilters: "",
                    //options: """
                    //     PARAM_1=value1
                    //    PARAM_2=value2
                    //     PARAM_3=
                    //     """,
                    rundeckInstance: "Rundeck-SME",
                    shouldFailTheBuild: true,
                    shouldWaitForRundeckJob: true,
                    tags: "",
                    tailLog: true])
                }
        
        
            }
        }
  }    


    
post {
        always {
          echo 'One way or another, I have finished'
        }
        success {
	  	    
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Esta ok !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n\n Uma nova versão da aplicação esta disponivel!!!")
        }
        unstable {
          
          telegramSend("O Build ${BUILD_DISPLAY_NAME} <${env.BUILD_URL}> - Esta instavel ...\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        failure {
          
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME}  - Quebrou. \nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        changed {
          echo 'Things were different before...'
        }
        aborted {
          
          telegramSend("O Build ${BUILD_DISPLAY_NAME} - Foi abortado.\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
    }
}
