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
- Web interface with copy-to-clipboard functionality
- Generates 2 prompts at a time
- Cyberpunk-inspired dark theme UI
- Characters: @obesewith.munky, @obesewith.glassy, @obesewith.yerm, @obesewith.teefred

## Tech Stack
- Python 3.11
- Flask 3.1.2
- HTML/CSS/JavaScript

## How to Use
1. Click "Generate Two Prompts" button
2. Two random video prompts will appear
3. Click "Copy" button under each prompt to copy to clipboard
4. Use the prompts with SORA AI video generation

## Recent Changes
- October 30, 2025: Converted from CLI script to Flask web app
- Added web interface with dark theme
- Implemented copy-to-clipboard functionality

## Workflow
- Flask development server runs on port 5000
- Web preview available in Replit
