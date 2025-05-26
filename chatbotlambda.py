import json
import boto3

def lambda_handler(event, context):
    try:
        if event.get("httpMethod") == "OPTIONS":
            return cors_response("CORS preflight successful")

        raw_body = event.get("body", "{}")
        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        mode = body.get("mode", "text")
        message = body.get("message", "")
        history = body.get("history", [])

        if not message:
            return error_response("Message is required.")

        bedrock = boto3.client("bedrock-runtime")

        if mode == "image":
            payload = {
                "textToImageParams": { "text": message },
                "taskType": "TEXT_IMAGE",
                "imageGenerationConfig": {
                    "cfgScale": 8,
                    "seed": 42,
                    "quality": "standard",
                    "width": 1024,
                    "height": 1024,
                    "numberOfImages": 1
                }
            }

            response = bedrock.invoke_model(
                modelId="amazon.titan-image-generator-v2:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )

            result = json.loads(response['body'].read())
            # ✅ Fix: Titan returns a list of base64 strings, not dictionaries
            base64_image = result['images'][0]
            return success_response({ "response": [{ "base64": base64_image }] })

        else:
            payload = {
                "inputText": message,
                "textGenerationConfig": {
                    "maxTokenCount": 512,
                    "temperature": 0.5,
                    "topP": 0.9
                }
            }

            response = bedrock.invoke_model(
                modelId="amazon.titan-text-express-v1",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )

            result = json.loads(response['body'].read())
            text = result['results'][0]['outputText']
            return success_response({ "response": text })

    except Exception as e:
        return error_response(str(e))


def success_response(data):
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        "body": json.dumps(data)
    }

def error_response(message):
    return {
        "statusCode": 500,
        "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        "body": json.dumps({ "response": f"Error: {message}" })
    }

def cors_response(message):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(message)
    }
