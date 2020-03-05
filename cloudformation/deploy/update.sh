aws cloudformation update-stack --stack-name "AsteroidsBackendNetworkStack2" --template-body file://../asteroids-backend-network.yaml
rm -Rf ../../services/lambda/layers/*
mkdir ../../services/lambda/layers/python/
mkdir ../../services/lambda/layers/python/common/
mkdir ../../services/lambda/layers/python/common/adapters/
mkdir ../../services/lambda/layers/python/common/domain/
pip3 install -r ../../requirements.txt -t ../../services/lambda/layers/python/
cp -r ../../services/common/adapters/ ../../services/lambda/layers/python/common/adapters
cp -r ../../services/common/domain/ ../../services/lambda/layers/python/common/domain
cp ../../services/common/configure.py ../../services/lambda/layers/python/common
sam package --template-file ../asteroids-backend-application.yaml --output-template-file ../output/asteroids-backend-application.yaml --s3-bucket sam.chuckbenger
aws cloudformation update-stack --stack-name "AsteroidsBackendApplicationStack" --template-body file://../output/asteroids-backend-application.yaml --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --parameters ParameterKey=VPC,ParameterValue=vpc-04fe4b01a40bd0390 ParameterKey=PublicSubnets,ParameterValue=subnet-01ed26efcc9ec19a1\\,subnet-045956dd037823caf ParameterKey=PrivateSubnets,ParameterValue=subnet-06254063960e02a44\\,subnet-0f59f8b3f07156417