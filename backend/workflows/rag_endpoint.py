import requests

def call_rag_endpoint(user_query):
    url = 'http://127.0.0.1:8000/api/chat/request'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example usage
user_query = "What is the capital of France?"
response = call_rag_endpoint(user_query)
print(response)