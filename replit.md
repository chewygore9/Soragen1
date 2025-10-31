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
- Style Cycler: Generates 5 variants of the same scene with different creative treatments
- **NEW: Snap Remix (Tyrone Style)**: Generate personality-driven video prompts with Tyrone-style narration
  - 3 personality modes: Calm (cinematic), Witty (sarcastic), Unhinged (pure chaos)
  - Uses snap_style_generator.json configuration
  - Includes themes, lighting, camera effects, and call-to-actions
- AI Generate: Uses GPT-4o to create creative prompts
- Remix Mode: Transform existing Sora videos with new creative treatments
- Download JSON: Save generated prompts as a JSON file for later use
- Character Database: Save and manage custom characters
- Cyberpunk-inspired dark theme UI
- Default Characters: @obesewith.munky, @obesewith.glassy, @obesewith.yerm, @obesewith.teefred, @obesewith.cookie, @obesewith.jamarcus
- **Sora API Integration**: Direct video generation support
  - **Kie.AI Sora 2 Pro**: Fully functional with direct API integration
  - **OpenAI Sora**: Ready for when API becomes public
  - Client-side API key management (keys stored securely in browser localStorage)
  - Configurable duration (5-20 seconds) and resolution (480p, 720p, 1080p)
  - Backend proxy route for Kie.AI to handle CORS and security

## Tech Stack
- Python 3.11
- Flask 3.1.2
- HTML/CSS/JavaScript

## How to Use

### Generate Two Prompts Mode
1. Click "Generate Two Prompts" button
2. Two random video prompts will appear
3. Click "Copy" button under each prompt to copy to clipboard

### Style Cycler Mode
1. Click "Style Cycler (5 Variants)" button
2. Generates 5 variants of the same base scene, dialogue, and cameos
3. Each variant has different camera, lighting, style, sound, and mood combinations
4. Click "Copy" under any variant to copy it to clipboard
5. Perfect for exploring different creative treatments of the same concept

### Download JSON
1. Generate prompts using either mode
2. Click "Download JSON File" button
3. Saves all generated prompts as `sora_prompts.json`
4. Includes all metadata (base scene, dialogue, cameos for Style Cycler mode)

## Recent Changes
- October 31, 2025: **MAJOR STABILITY UPDATE + SNAP REMIX + KIE.AI INTEGRATION**
  - Fixed database stability issues - app now runs smoothly even if database is unavailable
  - Disabled Flask auto-reload to prevent app restarts when switching apps
  - Added Snap Remix (Tyrone Style) feature with personality-driven prompts
  - Fixed Remix Mode copy button for textarea elements
  - Database now provides fallback characters when connection fails
  - **NEW: Kie.AI Sora 2 Pro Integration** - Fully functional video generation
  - API key management box with provider selection (OpenAI/Kie.AI)
  - Backend proxy route for secure Kie.AI API calls
  - Configurable video duration and resolution settings
- October 30, 2025 (Evening): Added JSON download feature to save prompts as files
- October 30, 2025 (PM): Added Style Cycler feature with 5-variant generation
- October 30, 2025: Converted from CLI script to Flask web app

## Workflow
- Flask development server runs on port 5000
- Web preview available in Replit
