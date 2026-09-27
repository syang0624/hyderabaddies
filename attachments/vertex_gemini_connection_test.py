# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai"]
# ///
"""Call Gemini locally"""

# Run this in your terminal first:
# gcloud auth application-default login

from google import genai


def main():
    # The SDK discovers ADC and handles access tokens automatically.
    with genai.Client(
        vertexai=True,
        project="YOUR_PROJECT_ID",  # Your team's Google Cloud project ID.
        location="us",
        http_options={"base_url": "https://aiplatform.us.rep.googleapis.com"},
    ) as client:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Reply with exactly: Connection test successful",
        )
        print(response.text)


if __name__ == "__main__":
    main()