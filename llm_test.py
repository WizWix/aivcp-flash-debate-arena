import os
import sys
import argparse
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def classify_sentiment(text):
    """
    Classifies the sentiment of the provided text as 'Positive', 'Negative', or 'Neutral'
    using the Gemini 2.5 Flash Lite model via the newer google.genai SDK.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables or .env file.")
        sys.exit(1)

    # Initialize the New Client
    client = genai.Client(api_key=api_key)

    # Model name
    model_id = "gemini-2.5-flash-lite"

    prompt = f"""
    Classify the sentiment of the following text as either 'Positive', 'Negative', or 'Neutral'.
    Output only the word 'Positive', 'Negative', or 'Neutral'.
    
    Text: "{text}"
    """

    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        sentiment = response.text.strip()

        # Basic validation of the output
        lowered = sentiment.lower()
        if "positive" in lowered:
            return "Positive"
        elif "negative" in lowered:
            return "Negative"
        elif "neutral" in lowered:
            return "Neutral"
        else:
            return f"Unknown ({sentiment})"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    # Pre-defined default phrase set
    default_phrases = [
        "I had a wonderful time at the park today!",
        "The food was cold and the service was slow.",
        "The new update is amazing and feature-rich.",
        "I'm really disappointed with the product's quality.",
        "The sky is blue and the grass is green.",
    ]

    parser = argparse.ArgumentParser(
        description="Classify text sentiment using Gemini LLM (google-genai)."
    )
    parser.add_argument(
        "input_text",
        nargs="?",
        help="The text to classify. If omitted, a random default phrase will be used.",
    )

    args = parser.parse_args()

    if args.input_text:
        text_to_classify = args.input_text
        print(f'Classifying input: "{text_to_classify}"')
    else:
        # Use the first one as default
        text_to_classify = default_phrases[0]
        print(f'No input provided. Using default phrase: "{text_to_classify}"')

    result = classify_sentiment(text_to_classify)
    print(f"Sentiment: {result}")


if __name__ == "__main__":
    main()
