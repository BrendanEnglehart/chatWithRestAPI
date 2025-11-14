# ChatWithRESTAPI
This is the REST API for the ChatWith Application. This should hold all of the backend control and model functions as well as any logic for connecting to external clients. This project runs Flask with FlaskRestX in the backend to make a RESTFul service and connect the client to the Database. 

# Current Features
## Models and Controllers
A number of models and controllers are implemented and are available in the RESTAPI, ideally in the future Messaging will be done through alternate protocols from the existing framework as it's not as functional for a chat framework

## Database connections
The app handles any connections to a MongoDB so long as the URI is set properly, ideally there is room to expand to other database frameworks by cleaning up some of the specific operations and generalizing them, but for now there isn't a plan to move to any new functionality in the near term. 

# Future Plans
## Chat Stream Changes
In the near term I want to switch out how the Chat logic is sent from client to server by spinning up a separate process to handle message streams and allow for a more active user interaction system. I haven't landed on a protocol to use yet, I am limited by trying to stay within a smaller cost system and keeping the free tiers in most of the external services. 

## Create a better deployment framework
I am using this as a portfolio project, so part of my plans involve adding a test and deploy method through github actions or some other means. As of right now I'm using internal builds but I would like to extend my build process into Github actions and build that way to make it a more modernized application. 

# How to Deploy
This is designed to be used with the github.com/BrendanEnglehart/chatWithFrontend application, however this is deployed independantly. In personal testing you will need to establish a MongoDB Database yourself and provide the URI in a `.env` file. After that you simply need to run `flask run --host=0.0.0.0 --port 5001` to get started. 