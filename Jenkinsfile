pipeline{
    agent any
    
    stages{

        stage('SCM'){
            steps{
                git credentialsId: 'github', 
                url: 'https://github.com/akshaymg99/SPE_Speech_Evaluator.git'
            }
        } 
 
	stage('Docker Build'){
            steps{
                sh "docker build . -t akshaymg99/speechspe:latest "
            }
        }   

            
    }
  
}
