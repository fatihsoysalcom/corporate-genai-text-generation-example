import os
import json
import urllib.request
import urllib.error

def generate_text_with_llm(prompt_text):
    """
    Uses an LLM API (e.g., OpenAI's GPT) to generate text based on a prompt.
    This demonstrates GenAI's application beyond product teams, for corporate use.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        return "API key missing."

    # Define the API endpoint and headers for a common LLM provider (OpenAI)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Define the payload for the API request
    # Using gpt-3.5-turbo as a cost-effective and capable model
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful corporate assistant."}, 
            {"role": "user", "content": prompt_text}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        # Encode the payload to JSON and then to bytes for the request body
        data = json.dumps(payload).encode("utf-8")

        # Create a Request object using urllib.request (standard library)
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        # Send the request and get the response
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            response_json = json.loads(response_body)

            # Extract the generated text from the API response
            if response_json.get("choices") and response_json["choices"][0].get("message"):
                generated_content = response_json["choices"][0]["message"]["content"].strip()
                return generated_content
            else:
                return f"Error: Unexpected API response format: {response_json}"

    except urllib.error.HTTPError as e:
        error_message = e.read().decode("utf-8")
        return f"HTTP Error: {e.code} - {error_message}"
    except urllib.error.URLError as e:
        return f"URL Error: {e.reason}"
    except json.JSONDecodeError:
        return "Error: Could not decode JSON response from API."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    # Example 1: Marketing department use case
    # This illustrates GenAI's role in corporate transformation beyond coding.
    marketing_prompt = (
        "Write a compelling short social media post (max 100 words) "
        "to announce a new eco-friendly smart home device that saves energy. "
        "Include relevant hashtags and a call to action."
    )

    print("Generating marketing copy using GenAI for a new product announcement...")
    generated_copy = generate_text_with_llm(marketing_prompt)
    print("\n--- Generated Marketing Content ---")
    print(generated_copy)
    print("\n-----------------------------------")

    # Example 2: Human Resources department use case
    # This further emphasizes the article's point about GenAI's versatility.
    hr_prompt = (
        "Draft a short, encouraging internal announcement (max 80 words) "
        "about a new company wellness program focusing on mental health. "
        "Emphasize confidentiality and support resources."
    )
    print("\nGenerating HR announcement using GenAI for a wellness program...")
    generated_hr_announcement = generate_text_with_llm(hr_prompt)
    print("\n--- Generated HR Announcement ---")
    print(generated_hr_announcement)
    print("\n---------------------------------")