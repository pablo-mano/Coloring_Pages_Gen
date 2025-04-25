# Coloring Pages Generator

A Python tool that generates creative coloring book prompts and organizes them for you. It uses OpenAI's models to create unique, concise prompts for coloring pages, and saves the results in organized folders.

## Features
- Generate multiple variations of coloring book prompts for a given theme
- Uses OpenAI GPT models for prompt generation
- Outputs prompts and results in organized folders
- Simple command-line interface

## Requirements
- Python 3.8+
- OpenAI API key

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/pablo-mano/Coloring_Pages_Gen.git
   cd Coloring_Pages_Gen
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Setup
Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage
Run the script from the command line. Example:
```sh
python generate_coloring_book.py --topic "Dinosaurs" --n 5
```
- `--topic` (or `-t`): The main theme for the coloring book prompts
- `--n`: Number of prompt variations to generate

The generated prompts and results will be saved in the `colourings/` folder, organized by theme and timestamp.

## Example
```
python generate_coloring_book.py --topic "Underwater Adventure" --n 3
```

## License
MIT License

---

Feel free to customize or extend this tool for your own coloring book projects!
