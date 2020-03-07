# Asteroids-Multiplayer-Backend

Python backend for the Asteroids Multiplayer backend. The goal of this was to experiment with AWS services and also try using a hexagonal architecture to abstract the details of the AWS services (SQS, Dynamo, Lambda) from the business logic.

## Architecture 

Here is how the architecture of the application is setup.

I would have made it high availability + put the game servers in a private subnet, but since this is something I want to leave up and not get a massive bill I decided to keep the design simple and cost efficient :)

![Image of Yaktocat](https://github.com/tkblackbelt/Asteroids-Multiplayer-Backend/raw/master/architecture.png)

## Authors

* **Charles Benger** - *Initial work* - [tkblackbelt](https://github.com/tkblackbelt)

## License

   Copyright 2019 Chuck Benger

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
