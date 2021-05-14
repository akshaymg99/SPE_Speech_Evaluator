pipeline{
    agent any
    
    stages{

        stage('SCM git pull'){
            steps{
                git credentialsId: 'github', 
                url: 'https://github.com/akshaymg99/SPE_Speech_Evaluator.git'
            }
        } 

	stage('Testing') {
	    steps{
		sh 'pip3 install Django==3.2'
		sh 'pip3 install python3'
		sh 'python3 manage.py test speech'		
	
	    }
	}
 
	stage('Docker Build'){
            steps{
                sh "docker build . -t akshaymg99/speech-spe:latest "
            }
        }
	stage('DockerHub Push'){
            steps{
                withCredentials([string(credentialsId: 'docker-hub', variable: 'dockerHubPwd')]) {
                    sh "docker login -u akshaymg99 -p ${dockerHubPwd}"
                }
                sh "docker push akshaymg99/speech-spe:latest "
            }
            
        }   

            
    }
  
}
