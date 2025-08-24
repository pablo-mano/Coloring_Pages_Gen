from openai import OpenAI
from dotenv import dotenv_values
import base64
import json
import argparse
import os
import sys
import re
import time
from datetime import datetime

# Ensure UTF-8 encoding for output (important for non-ASCII prompts)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Load OpenAI API key from backend/.env, .env, or environment
from pathlib import Path

def load_api_key():
    # Try backend/.env
    backend_env = Path(__file__).parent / ".env"
    if backend_env.exists():
        env_vars = dotenv_values(str(backend_env))
        if env_vars.get("OPENAI_API_KEY"):
            return env_vars.get("OPENAI_API_KEY")
    # Try project root .env
    root_env = Path(__file__).parent.parent / ".env"
    if root_env.exists():
        env_vars = dotenv_values(str(root_env))
        if env_vars.get("OPENAI_API_KEY"):
            return env_vars.get("OPENAI_API_KEY")
    # Fallback to environment
    return os.getenv("OPENAI_API_KEY")

api_key = load_api_key()
client = OpenAI(api_key=api_key)

def generate_variations(main_prompt, number_of_pages):
    """
    Generate number_of_pages prompt variations for a coloring book theme using OpenAI chat completion.
    Returns a list of prompt strings.
    """
    print("\n=== Step 1/4: Generating Prompt Variations ===")
    print(f"[INFO] Requesting {number_of_pages} prompt variations for theme: '{main_prompt}'")
    print(f"[STATUS] Starting prompt generation at {datetime.now().strftime('%H:%M:%S')}")
    print("-"*50)
    start_time = time.time()
    messages = [
        {"role": "system", "content": (
            "You are a helpful assistant that creates concise coloring book prompts. "
            "Please always include instruction first: 'Generate an image which is colouring. "
            "Use only black colour for lines and white for inside of objects. "
            "Extend picture with small signature at the bottom right of the picture \"Pablo Mano\".'"
        )},
        {'role': 'user', 'content': (
            f'Please generate {number_of_pages} different variations of a coloring book prompt for the main theme: "{main_prompt}" '
            'as a JSON array. Example: {"prompts" : ["prompt 1", "prompt 2", "prompt 3" ]}'
        )}
    ]
    content = ""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        # Extract prompts from JSON response
        if isinstance(data, dict) and "prompts" in data:
            prompts = data["prompts"]
        elif isinstance(data, list):
            prompts = data
        else:
            raise ValueError(f"Unexpected response format from GPT-4o: {data}")
        elapsed = time.time() - start_time
        print(f"✔ Successfully generated {len(prompts)} prompt variations in {elapsed:.1f}s")
    except Exception as e:
        print(f"✖ Error parsing prompts from GPT-4o: {e}\nRaw content: {content}")
        # Fallback: try extracting prompts from lines
        prompts = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
        elapsed = time.time() - start_time
        print(f"[WARN] Fallback: extracted {len(prompts)} prompt(s) from raw content in {elapsed:.1f}s")
    print(f"{'='*60}\n")
    return prompts

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Colouring Page Generator - Progress Output")
    print("="*60)

    # Parse command-line arguments for theme and image count
    print("[INFO] Parsing command-line arguments...")
    parser = argparse.ArgumentParser(description="Generate coloring book images.")
    parser.add_argument("-t", "--theme", required=True, help="Main coloring topic")
    parser.add_argument("--number-of-pages", type=int, default=3, help="Number of images to generate (default: 3)")
    args = parser.parse_args()

    main_topic = args.theme
    n_images = args.number_of_pages
    print(f"[INFO] Theme: {main_topic}")
    print(f"[INFO] Number of images to generate: {n_images}")
    print("-"*60)

    # Generate prompt variations for the given theme
    variations = generate_variations(main_topic, n_images)

    def short_ascii(text, maxlen=16):
        """
        Convert theme name to a short, safe folder name (alphanumeric/underscore, max length).
        Polish characters are replaced with their ASCII equivalents (e.g., ż→z, ą→a).
        """
        # Mapping of Polish characters to ASCII equivalents
        polish_map = str.maketrans({
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o',
            'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O',
            'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
        })
        text_ascii = text.translate(polish_map)
        return re.sub(r'[^a-zA-Z0-9_]', '', text_ascii.replace(' ', '_'))[:maxlen]

    theme_short = short_ascii(main_topic)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Create output directory for the theme if it doesn't exist
    output_dir = os.path.join("colourings", theme_short)
    if not os.path.exists(output_dir):
        print(f"[INFO] Creating output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    print(f"[INFO] Output directory ready: {output_dir}")
    print("-"*60)

    # Generate and save images for each prompt variation
    print("=== Step 2/4: Generating Images ===")
    print(f"[STATUS] Starting image generation at {datetime.now().strftime('%H:%M:%S')}")
    print(f"[INFO] Will generate {len(variations)} images")
    print("-"*50)
    image_files = []
    generation_start_time = time.time()
    
    for idx, prompt in enumerate(variations, 1):
        progress_pct = (idx-1) / len(variations) * 100
        print(f"[INFO] ({idx}/{len(variations)}) [{progress_pct:.0f}%] Generating image for prompt:")
        print(f"    → {prompt}")
        img_start_time = time.time()
        if not isinstance(prompt, str):
            print(f"[WARN] Skipping non-string prompt #{idx}: {prompt}")
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
            image_files.append(filename)
            img_elapsed = time.time() - img_start_time
            print(f"  ✔ Saved: {filename} (generated in {img_elapsed:.1f}s)")
        except Exception as e:
            img_elapsed = time.time() - img_start_time
            print(f"  ✖ Skipping prompt #{idx} due to error after {img_elapsed:.1f}s: {e}")
            print(f"    Prompt: {prompt}")
    
    generation_elapsed = time.time() - generation_start_time
    success_rate = len(image_files) / len(variations) * 100 if variations else 0
    print(f"[SUMMARY] Generated {len(image_files)}/{len(variations)} images ({success_rate:.0f}% success) in {generation_elapsed:.1f}s")
    print("-"*60)

    # Step: Combine all images into a single PDF
    print("=== Step 3/4: Creating PDF with all images ===")
    print(f"[STATUS] Starting PDF creation at {datetime.now().strftime('%H:%M:%S')}")
    pdf_start_time = time.time()
    try:
        from PIL import Image
        pdf_path = os.path.join(output_dir, f"colouring_{theme_short}_{timestamp}.pdf")
        pil_images = []
        for img_file in image_files:
            img = Image.open(img_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            pil_images.append(img)
        if pil_images:
            print(f"[INFO] Combining {len(pil_images)} images into PDF...")
            pil_images[0].save(pdf_path, save_all=True, append_images=pil_images[1:])
            pdf_elapsed = time.time() - pdf_start_time
            print(f"  ✔ PDF created: {pdf_path} (in {pdf_elapsed:.1f}s)")
        else:
            print("  ✖ No images to add to PDF.")
    except ImportError:
        print("  ✖ Pillow (PIL) is not installed. Install it with 'pip install pillow' to enable PDF creation.")
    except Exception as e:
        pdf_elapsed = time.time() - pdf_start_time
        print(f"  ✖ Failed to create PDF after {pdf_elapsed:.1f}s: {e}")
    print("-"*60)
    
    # Final summary with total time
    total_elapsed = time.time() - generation_start_time
    print("=== Step 4/4: Generation Complete! ===")
    print(f"[SUMMARY] Generated {len(image_files)} images and PDF for theme '{main_topic}'")
    print(f"[TIMING] Total processing time: {total_elapsed:.1f}s")
    print(f"[TIMING] Average time per image: {total_elapsed/len(image_files):.1f}s" if image_files else "[TIMING] No images generated")
    print(f"[OUTPUT] Folder: {output_dir}")
    print(f"[STATUS] Completed at {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)