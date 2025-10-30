# SORA Wild Style Generator

## Overview
A Flask web application that generates random creative video prompts for SORA AI video generation. The generator combines various cinematic elements including scenes, camera movements, lighting, styles, dialogue, sound, and mood to create unique prompt combinations.

## Project Structure
```
SoraWildStyleGen/
├── main.py              # Flask app with prompt generation logic
├── templates/
│   └── index.html       # Web interface
└── static/              # (optional) for additional CSS/JS
```

## Features
- Random prompt generation combining multiple creative elements
- **AI Generate (GPT-4)**: LLM-powered creative prompt generation for truly unique, never-repeating content
- Web interface with copy-to-clipboard functionality
- Generates 2 prompts at a time
- Style Cycler: Generates 5 variants of the same scene with different creative treatments
- Remix Mode: Recreate existing Sora videos with new characters and creative settings
- Custom Character Database: Save and reuse your Sora character names permanently
- Vibe Pack Presets: Save and load custom style configurations (localStorage)
- Download JSON: Save generated prompts as a JSON file with metadata (creator, timestamp, version, notes)
- Cyberpunk-inspired dark theme UI
- Default Characters: @obesewith.munky, @obesewith.glassy, @obesewith.yerm, @obesewith.teefred

## Tech Stack
- Python 3.11
- Flask 3.1.2
- PostgreSQL (optional, for custom character storage)
- psycopg2-binary
- HTML/CSS/JavaScript

## Database Setup (Optional)
The Custom Character Database feature requires PostgreSQL:
- The app automatically detects if `DATABASE_URL` environment variable is set
- If database is not configured, character saving features will gracefully degrade
- The app will run normally without a database; all other features remain functional

## How to Use

### Generate Two Prompts Mode
1. Click "Generate Two Prompts" button
2. Two random video prompts will appear (pulled from hardcoded library)
3. Click "Copy" button under each prompt to copy to clipboard

### AI Generate Mode (NEW!)
1. Click "AI Generate (GPT-4)" button
2. GPT-4o creates 2 completely unique, creative prompts from scratch
3. Never repeats - infinite variety with wild, surreal scenarios
4. Powered by Replit AI Integrations (charges billed to your Replit credits)
5. Click "Copy" under any prompt to copy it to clipboard

### Style Cycler Mode
1. Click "Style Cycler (5 Variants)" button
2. Generates 5 variants of the same base scene, dialogue, and cameos
3. Each variant has different camera, lighting, style, sound, and mood combinations
4. Click "Copy" under any variant to copy it to clipboard
5. Perfect for exploring different creative treatments of the same concept

### Download JSON
1. Optionally add project notes in the text field (e.g., "Weekend TikTok dropset, bayou noir vibe")
2. Generate prompts using either mode
3. Click "Download JSON File" button
4. Saves all generated prompts as `sora_prompts.json` with metadata:
   - Creator: @obesewitherspooon
   - Generated timestamp
   - Version: v2.0
   - Your project notes
   - All prompt data (includes base scene, dialogue, cameos for Style Cycler mode)

### Save Custom Characters
1. Enter character names (comma-separated) in the text box
2. Click "Save to Database" button
3. Characters are permanently stored in PostgreSQL database
4. View all saved characters below the save box
5. Use saved characters in Remix Mode

### Remix Mode
1. Click "Remix Mode" button to toggle the Sora Remix Station
2. Paste the Sora video link in Box 1
3. Add your remix "ingredients" as JSON in Box 2:
   - Example: `{"characters":["@bonniebluexo"], "style":"Neon Noir", "lighting":"sunset orange haze", "camera":"low angle slow push", "music":"1990s Louisiana gangster rap", "mood":"moody romantic tension"}`
4. Click "Save Remix Preset" to save your setup to localStorage for later
5. Click "Load Preset" to reload a saved remix configuration
6. Click "Remix It!" to generate your final Sora remix prompt
7. Copy the generated remix prompt to use in Sora

## Recent Changes
- October 30, 2025 (Late Evening): Added AI Generate mode with GPT-4o for unlimited creative variety (Replit AI Integrations)
- October 30, 2025 (Late Evening): Simplified Remix Mode to use JSON input format (2 boxes instead of multiple fields)
- October 30, 2025 (Late Evening): Added Custom Character Database with PostgreSQL for permanent character storage
- October 30, 2025 (Late Evening): Added Remix Mode to recreate Sora videos with new characters and style settings
- October 30, 2025 (Late Evening): Added Vibe Pack preset save/load functionality (localStorage)
- October 30, 2025 (Evening): Added metadata to JSON downloads (creator, timestamp, version, project notes)
- October 30, 2025 (Evening): Added JSON download feature to save prompts as files
- October 30, 2025 (PM): Added Style Cycler feature with 5-variant generation
- October 30, 2025: Converted from CLI script to Flask web app
- Added web interface with dark theme
- Implemented copy-to-clipboard functionality

## Workflow
- Flask development server runs on port 5000
- Web preview available in Replit
