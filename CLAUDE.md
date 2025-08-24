# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Coloring Pages Generator application with a Python command-line tool and a full-stack web application. It uses OpenAI's DALL-E model to generate custom coloring book pages based on user themes.

## Architecture

The project has three main components:

1. **Standalone Python Script** (`generate_coloring_book.py`): Command-line tool for direct coloring page generation
2. **Frontend** (`frontend/`): React application with Material-UI for the web interface  
3. **Backend** (`backend/`): Node.js/Express API server that wraps the Python generation script

## Common Commands

### Python Script (Standalone)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Generate coloring pages
python generate_coloring_book.py --topic "Dinosaurs" --n 5
```

### Frontend Development
```bash
cd frontend
npm install
npm start          # Development server
npm run build      # Production build
```

### Backend Development  
```bash
cd backend
npm install
node index.js      # Start API server on port 5000
```

## Environment Setup

The project requires an OpenAI API key. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key_here
```

The Python script checks multiple locations for the API key:
1. `backend/.env`  
2. Project root `.env`
3. Environment variable `OPENAI_API_KEY`

## Key Architecture Details

### Frontend Structure
- Uses React Router for navigation between pages: Home, Generator, Payment, Dashboard, Auth
- Protected by simple password authentication (demo password: "test123")
- Material-UI components for consistent styling
- Communicates with backend API for coloring page generation

### Backend API
- Express server with CORS enabled
- Main endpoint: `POST /generate` - accepts theme and count, returns generation results
- Wraps the Python script execution via child process
- Returns both output directory and generation logs

### Generation Engine
The Python script (`generate_coloring_book.py`) handles the core generation logic:
- Uses OpenAI GPT models to create prompt variations
- Generates images using DALL-E with specific coloring book formatting
- Creates PDF compilations of generated pages
- Organizes output in timestamped folders under `colourings/`

### Output Structure
Generated content is saved to `colourings/{theme}_{timestamp}/` with:
- Individual PNG images
- Combined PDF coloring book
- Metadata and prompts used

## Development Notes

- The frontend is deployed to Netlify with password protection
- Backend deployment is planned for Render/Railway/Heroku
- Database integration and payment system (Stripe) are planned but not yet implemented
- The current implementation is a working MVP with the core generation functionality complete