from openai import OpenAI
from dotenv import dotenv_values
import base64
import json
import argparse
import os
import sys
import re
from datetime import datetime

# Ensure UTF-8 encoding for output (important for non-ASCII prompts)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Load OpenAI API key from .env or environment
env_vars = dotenv_values(".env")
api_key = env_vars.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_variations(main_prompt, n):
    """
    Generate n prompt variations for a coloring book theme using OpenAI chat completion.
    Returns a list of prompt strings.
    """
    messages = [
        # System prompt: instructs the assistant to generate coloring prompts with signature
        {"role": "system", "content": (
            "You are a helpful assistant that creates concise coloring book prompts. "
            "Please always include instruction first: 'Generate an image which is colouring. "
            "Use only black colour for lines and white for inside of objects. "
            "Extend picture with small signature at the bottom right of the picture \"Pablo Mano\".'"
        )},
        # User prompt: requests n variations for the given theme
        {'role': 'user', 'content': (
            f'Please generate {n} different variations of a coloring book prompt for the main theme: "{main_prompt}" '
            'as a JSON array. Example: {"prompts" : ["prompt 1", "prompt 2", "prompt 3" ]}'
        )}
    ]
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        print(data)
        # Extract prompts from JSON response
        if isinstance(data, dict) and "prompts" in data:
            prompts = data["prompts"]
        elif isinstance(data, list):
            prompts = data
        else:
            raise ValueError(f"Unexpected response format from GPT-4o: {data}")
    except Exception as e:
        print(f"Error parsing prompts from GPT-4o: {e}\nRaw content: {content}")
        # Fallback: try extracting prompts from lines
        prompts = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
    return prompts

if __name__ == "__main__":
    # Parse command-line arguments for theme and image count
    parser = argparse.ArgumentParser(description="Generate coloring book images.")
    parser.add_argument("-t", "--theme", required=True, help="Main coloring topic")
    parser.add_argument("-n", "--count", type=int, default=3, help="Number of images to generate")
    args = parser.parse_args()

    main_topic = args.theme
    n_images = args.count

    # Generate prompt variations for the given theme
    variations = generate_variations(main_topic, n_images)

    def short_ascii(text, maxlen=16):
        """Convert theme name to a short, safe folder name (alphanumeric/underscore, max length)."""
        return re.sub(r'[^a-zA-Z0-9_]', '', text.replace(' ', '_'))[:maxlen]

    theme_short = short_ascii(main_topic)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Create output directory for the theme if it doesn't exist
    output_dir = os.path.join("colourings", theme_short)
    os.makedirs(output_dir, exist_ok=True)

    # Generate and save images for each prompt variation
    for idx, prompt in enumerate(variations, 1):
        if not isinstance(prompt, str):
            print(f"Skipping non-string prompt #{idx}: {prompt}")
            continue
        try:
            # Generate image using OpenAI API
            result = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                quality="auto",
                size="1024x1536",
                n=1
            )
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            # Save image to theme subfolder with timestamp and index
            filename = os.path.join(output_dir, f"colouring_{theme_short}_{timestamp}_{idx}.png")
            with open(filename, "wb") as f:
                f.write(image_bytes)
            print(f"Saved {filename} for prompt: {prompt}")
        except Exception as e:
            print(f"Skipping prompt #{idx} due to error: {e}\nPrompt: {prompt}")