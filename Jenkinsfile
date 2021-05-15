pipeline{
    agent any
    
    stages{

        stage('SCM git pull'){
            steps{
                git credentialsId: 'github', 
                url: 'https://github.com/akshaymg99/SPE_Speech_Evaluator.git'
            }
        } 

	stage('Docker Build'){
            steps{
                sh "docker build . -t akshaymg99/speech-spe:latest "
            }
        }
	
	stage('Testing') {
	    steps{
		sh 'ls -l'
		sh 'python3 manage.py test'		
	    }

	    agent {
	       docker {
	         image 'akshaymg99/speech-spe:latest'
	         }
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
