import os, requests, json

def chat_llm(prompt: str, model= 'gpt-4o-mini'):
    url= "https://openrouter.ai/api/v1/chat/completions"
    openrouter_api_key= os.getenv("OPENROUTER_API_KEY")
    headers= {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openrouter_api_key}"
    }
    data= {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response= requests.post(url, headers=headers, json=data)

    # Check for HTTP errors
    if response.status_code != 200:
        print("Request failed!")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        raise Exception("LLM call failed.")

    try:
        json_data = response.json()

        # Print full response if debugging
        print("LLM Response:", json_data)

        if "choices" in json_data:
            return json_data["choices"][0]["message"]["content"]
        elif "error" in json_data:
            raise Exception(f"LLM error: {json_data['error']}")
        else:
            raise Exception(f"Unexpected response: {json_data}")
    except Exception as e:
        raise RuntimeError(f"Failed to parse LLM response: {e}")