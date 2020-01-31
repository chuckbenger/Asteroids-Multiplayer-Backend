aws cloudformation create-stack --stack-name "AsteroidsBackendNetworkStack" --template-body file://../asteroids-backend-network.yaml
aws cloudformation create-stack --stack-name "AsteroidsBackendAuthenticationStack" --template-body file://../asteroids-backend-authentication.yaml --parameters ParameterKey=CognitoDomain,ParameterValue=chuckbenger
sam package --template-file ../asteroids-backend-application.yaml --output-template-file ../output/asteroids-backend-application.yaml --s3-bucket sam.chuckbenger
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
aws cloudformation create-stack --stack-name "AsteroidsBackendApplicationStack" --template-body file://../output/asteroids-backend-application.yaml --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --parameters ParameterKey=AuthenticationStackName,ParameterValue=AsteroidsBackendAuthenticationStack