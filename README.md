Build a Serverless AI Chatbot with Amazon Bedrock, Lambda, API Gateway & S3 🤖


Serverless AI Chatbot using Amazon Bedrock
Build this hands-on demo step by step with my detailed tutorial on Julien Muke YouTube. Feel free to subscribe 🔔!
Tutorial

This repository contains the steps corresponding to an in-depth tutorial available on my YouTube channel, Julien Muke.

If you prefer visual learning, this is the perfect resource for you. Follow my tutorial to learn how to build projects like these step-by-step in a beginner-friendly manner!

Introduction

In this step-by-step tutorial, you'll learn how to create a powerful serverless AI Chatbot using Amazon Bedrock's Titan Text G1 - Express LLM. We’ll connect it to AWS Lambda, expose it via API Gateway with proper CORS handling, and deploy a beautiful HTML/JavaScript frontend using S3 static website hosting.
Overview

Users interact with the chatbot either through a static frontend hosted on Amazon S3 or Amplify Hosting or by calling the API directly.

Their messages are sent as HTTPS requests to Amazon API Gateway, which securely forwards them to an AWS Lambda function.

The Lambda function processes the input and uses an IAM Role to securely call Amazon Bedrock, invoking the Titan model to generate a chatbot response.

That response flows back through Lambda and API Gateway to the user.
Tech Stack:

• Amazon Bedrock (Titan Text G1 - Express)
• AWS Lambda
• Amazon API Gateway
• Amazon S3 (Static Hosting)
• JavaScript + HTML + CSS
➡️ Step 1 - Set Up Amazon Bedrock Access

Make sure your AWS account has Bedrock access (Bedrock is GA now but some regions might differ — N. Virginia us-east-1 is safest).

    Go to the AWS Console → Amazon Bedrock
    Request access to amazon.titan-text-express-v1 you can also choose any models you want to use based on your needs.

Image

    Once approved, you're ready to build

Image
➡️ Step 2 - Create an IAM Role for Lambda

To create an IAM role with the console:

    In the navigation pane search for IAM, choose Roles, and then choose Create role.
    For Trusted entity type, choose AWS service
    For Service or use case, choose a service Lambda then Choose Next.
    For Permissions policies, the options depend on the use case that you selected, for this demo select these permissions:
    • AmazonBedrockFullAccess
    • CloudWatchLogsFullAccess
    For Role name, enter chatBotLambdaRole
    Review the role, and then choose Create role.

➡️ Step 3 - Create the Lambda Function

To create a Lambda function with the console:

    In the navigation pane search for Lambda function
    Choose Create function.
    Select Author from scratch.
    In the Basic information pane, for Function name, enter chatbotlambda
    For Runtime, choose Python 3.12 (easiest for Bedrock SDK usage).
    Leave architecture set to x86_64, and then choose Create function.
    For the Lambda function code, copy and paste the code below into your Lambda code editor:

lambda_function.py

Note: This function will;
Accepts a message from the user
Sends it to a Bedrock LLM
Returns the model's response
➡️ Step 4 - Set Up API Gateway

We're will create a REST API, the REST API provides an HTTP endpoint for your Lambda function. API Gateway routes requests to your Lambda function, and then returns the function's response to clients.

    In the navigation pane search for API Gateway, choose REST API, click "Build"
    Choose Create API, enter a name chatbot-api click "Create API".
    Once the REST API is created, click on "Create Resource"
    Enter a resource, i'll enter chat
    Make sure you Enable CORS (Cross Origin Resource Sharing), which will create an OPTIONS method that allows all origins, all methods, and several common headers.
    Once the resource is created, click on "Create method"
    For the method type, choose POST
    For the integration type choose "Lambda function"
    Make sure you Enable Lambda proxy integration to send the request to your Lambda function as a structured event.
    Choose the your regoin us-east-1 then choose your existing Lambda function that you created earlier.
    Keep everything as default then click "Create method"
    Back resources, click on "Deploy API"
    For the deploy stage, create a new stage, i'll name it dev then click on "Deploy"

Test API Gateway

Deploy your API and test using Postman or curl

⚠️Note: Once it's deployed successfully, we'll have an invoke URL that will be our API endpoint, we're going to call it and then it's going to call the Lambda function to generate the response to us so.
➡️ Step 5 - Build the Frontend Chat UI

Build a stylish chat interface using pure HTML + CSS + JavaScript — no frameworks, easy to deploy via S3 or Amplify. I have a sample that we'll use for this tutorial, feel free to copy and use it for this demo.

    Open your code editor (VS Code)
    Create an index.html file
    Copy and paste the code below

index.html

⚠️Note: Replace https://your-api-id.execute-api.us-east-1.amazonaws.com/chat with your real API Gateway endpoint.
➡️ Step 6 - Deploy Frontend Chat UI to an S3 Static Website

We'll deploy our fully serverless AI chatbot to S3 for static website hosting.

    In the AWS Management Console, navigate to Amazon S3, click on "Create Bucket"
    For General configuration, choose choose General purpose buckets.
    Enter a unique bucket name, i'll name myaichatbotdemo
    Make sure you disable "Block all public access" to have public access.
    Keep everything else as default and click "Create bucket"
    Upload the index.html file that you created in step 5
    Go to "Properties" and scroll down to "Static Website Hosting" and click on "Edit"
    Under "Static Website Hosting", choose "Enable"
    Specify index.html as the index document, then click "Save"
    Go to "Permissions" under Bucket Policy click "Edit"
    Paste the Bucket Policy below, that grants read-only access to all objects (s3:GetObject) inside a specific S3 bucket.

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}

⚠️Note: Replace your-bucket-name with your actual bucket name, then click "Save"

    Go back to the S3 Bucket console, choose Objects, then click on index.html
    To visit your fully serverless AI chatbot Live, click on the Object URL.
    You should see your AI Chatbot with a stylish chat interface running on Amazon S3.

🏆 Now you can ask the AI Chatbot anything and you will have a real-time AI responses.
🗑️ Clean Up Resources
When you’re done, clean up your AWS resources to avoid charges.
