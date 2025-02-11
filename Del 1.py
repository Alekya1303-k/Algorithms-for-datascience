import json
import validators
import requests

def evaluate_url(url):
    """
    Evaluates a given URL and returns a JSON object with a score and explanation.
    
    :param url: The URL to evaluate.
    :return: JSON object containing a score (float) and explanation (string).
    """
    if not validators.url(url):
        return json.dumps({
            "score": 0.0,
            "explanation": "Invalid URL format."
        })
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        status_code = response.status_code
        
        if 200 <= status_code < 400:
            score = 1.0
            explanation = "URL is accessible and returns a valid response."
        else:
            score = 0.5
            explanation = f"URL returned status code {status_code}. It may not be reliable."
    except requests.exceptions.RequestException as e:
        score = 0.0
        explanation = f"Error accessing URL: {str(e)}"
    
    return json.dumps({
        "score": score,
        "explanation": explanation
    })

# Initial testing
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "https://www.nonexistentwebsite123456.com",
        "not_a_valid_url"
    ]
    
    for url in test_urls:
        print(evaluate_url(url))
