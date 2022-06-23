pipeline {
    agent any
    stages {
        stage('clone') {
            steps {
		echo "Cloning Git"
		sh "rm -rf /var/lib/jenkins/cvat_data"
		sh "mkdir /var/lib/jenkins/cvat_data"
		sh "cd /var/lib/jenkins/cvat_data ; git clone http://10.40.41.57:7990/scm/cvat/cvat-dev.git"
		
            }



        }



        stage('Build') {

            steps {

                sh "cd /var/lib/jenkins/cvat_data/cvat-dev/; docker-compose -f docker-compose.yml -f docker-compose.dev.yml build"

            }



        }



	stage('Test') {

            steps {

                script {

		sh "echo Testing...."

                }

            }

        }



        stage('Deploy') {

            steps {

		echo "Deploy.."
		
                sh "cd /var/lib/jenkins/cvat_data/cvat-dev/ && docker-compose down"
	        sh "docker rm -f '\$(docker ps -aq | grep -v bitbucket)'"
                sh "cd /var/lib/jenkins/cvat_data/cvat-dev/ && docker-compose up -d"
		



            }



        }



    }



}
