from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
import random, json, io, os, requests
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI

app = Flask(__name__)

# ==== OPENAI SETUP ====
AI_ENABLED = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY") is not None
if AI_ENABLED:
    client = OpenAI(
        api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY"),
        base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")
    )
else:
    client = None

# ==== SORA API SETUP ====
SORA_ENABLED = os.environ.get("SORA_API_KEY") is not None
SORA_API_KEY = os.environ.get("SORA_API_KEY")
if SORA_ENABLED:
    # Sora uses OpenAI client but with specific endpoint
    sora_client = OpenAI(
        api_key=SORA_API_KEY,
        # Sora API endpoint - may need adjustment when API is public
        base_url="https://api.openai.com/v1"
    )
else:
    sora_client = None

# ==== DATABASE SETUP ====
DB_ENABLED = False  # Start with disabled
DB_URL = os.environ.get('DATABASE_URL')

def test_db_connection():
    """Test if database is actually available"""
    global DB_ENABLED
    if not DB_URL:
        print("No DATABASE_URL found - database features disabled")
        DB_ENABLED = False
        return False
    
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=3)
        conn.close()
        DB_ENABLED = True
        print("Database connection successful")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("App will run without database features")
        DB_ENABLED = False
        return False

def get_db_connection():
    if not DB_ENABLED or not DB_URL:
        return None
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database if available"""
    if not test_db_connection():
        return
    
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS custom_characters (
                id SERIAL PRIMARY KEY,
                character_name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Database initialization warning: {e}")
        DB_ENABLED = False

# Initialize database but don't crash if it fails
init_db()

# ==== PROMPT BANKS ====
scene_options = [
    "A foggy bayou shack glowing with neon lights and mosquitos orbiting the lamp.",
    "Inside a Waffle House at 3AM after a failed heist.",
    "Munky and Glassy arguing in a busted UFO that crash-landed in a Walmart parking lot.",
    "Yerm preaching about loyalty while Tee Fred counts cash on a swamp boat.",
    "A therapy circle in the middle of the bayou surrounded by talking frogs.",
    "A 1990s rap video being filmed during a thunderstorm.",
    "Post-apocalyptic gas station run by an alligator in sunglasses.",
    "Glassy floating through outer space trying to light himself.",
    "Munky accidentally becomes president of a reptile biker gang.",
    "Yerm trapped inside a microwave trying to negotiate peace with it."
]

cameos_options = [
    ["@obesewith.munky"],
    ["@obesewith.glassy"],
    ["@obesewith.yerm"],
    ["@obesewith.teefred"],
    ["@obesewith.munky", "@obesewith.glassy"],
    ["@obesewith.teefred", "@obesewith.yerm"],
    ["@obesewith.munky", "@obesewith.glassy", "@obesewith.teefred"],
    ["@obesewith.munky", "@obesewith.glassy", "@obesewith.yerm", "@obesewith.teefred"]
]

camera_options = [
    "handheld documentary zooms with sudden whip-pans",
    "smooth tracking shot through fog and neon reflections",
    "360-degree orbit with glitch transitions",
    "slow dolly push-in with extreme depth of field",
    "chaotic drone flyby that crashes mid-shot",
    "comic-book panel transitions with onomatopoeia overlays",
    "cinematic over-the-shoulder crosscut with lens flares",
    "stop-motion stutter camera movement like an old VHS"
]

lighting_options = [
    "neon pink and teal glow reflecting off water",
    "warm golden sunlight breaking through swamp fog",
    "flickering fluorescent gas-station lights with bug shadows",
    "blacklight haze with glowing smoke effects",
    "high-contrast noir red and blue tones",
    "psychedelic rainbow palette, pulsing with bass beats",
    "storm lightning flashes illuminating silhouettes",
    "retro CRT color bleed and static overlay"
]

style_options = [
    "Adult Swim absurdist comedy",
    "Louisiana swamp noir",
    "vaporwave retro animation",
    "1990s gangster rap video",
    "mockumentary handheld realism",
    "trippy psychedelic dream sequence",
    "animated claymation chaos",
    "GTA loading-screen cinematic"
]

dialogue_options = [
    "You ever seen smoke argue back? That's when I knew I was chosen.",
    "Down here, loyalty's like gator teeth — sharp till it breaks.",
    "I ain't paranoid if they really cloning me.",
    "Sometimes I dream in 480p, bro.",
    "Munky, stop touching buttons you don't understand!",
    "If it's glowing, that means it's money… or radiation.",
    "This swamp got more secrets than my search history.",
    "They told me I couldn't be two things at once — so I became three."
]

sound_options = [
    "slow trap beat with frogs croaking in rhythm",
    "distorted gospel choir with low 808 rumble",
    "lofi jazz sample with cicada ambience",
    "swampy blues guitar riff blended with crickets",
    "synthwave arpeggio with dripping water FX",
    "random trumpet blasts and street noises",
    "heavy bassline synced with lightning strikes",
    "banjo trap remix with vinyl crackle"
]

mood_options = [
    "chaotic and hilarious",
    "grimly cinematic and serious",
    "trippy and dreamlike",
    "lazy swamp summer energy",
    "paranoid but comedic",
    "surreal and melancholy",
    "loud, wild, and unhinged",
    "sincere but ridiculous"
]

# ==== RANDOMIZER FUNCTION ====
def generate_prompt():
    return {
        "model": "sora-2",
        "size": "1280x720",
        "seconds": random.choice([10, 11, 12]),
        "prompt": {
            "scene": random.choice(scene_options),
            "cameos": random.choice(cameos_options),
            "camera": random.choice(camera_options),
            "lighting": random.choice(lighting_options),
            "style": random.choice(style_options),
            "dialogue": random.choice(dialogue_options),
            "sound": random.choice(sound_options),
            "mood": random.choice(mood_options)
        }
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simple')
def simple():
    """Simple, streamlined video generation interface"""
    return render_template('simple.html')

@app.route('/snap-standalone')
def snap_standalone():
    """Serve the standalone Snap Remix Station"""
    return send_file('snap_remix_standalone.html')

@app.route('/generate')
def generate():
    prompts = [generate_prompt() for _ in range(2)]
    return jsonify(prompts)

@app.route("/cycle", methods=["POST"])
def cycle():
    data = request.get_json()
    base_scene = random.choice(scene_options)
    cameos = random.choice(cameos_options)
    base_dialogue = random.choice(dialogue_options)

    variants = []
    for _ in range(5):
        variant = {
            "model": "sora-2",
            "size": "1280x720",
            "seconds": random.choice([10, 11, 12]),
            "prompt": {
                "scene": base_scene,
                "cameos": cameos,
                "camera": random.choice(camera_options),
                "lighting": random.choice(lighting_options),
                "style": random.choice(style_options),
                "dialogue": base_dialogue,
                "sound": random.choice(sound_options),
                "mood": random.choice(mood_options)
            }
        }
        variants.append(variant)

    return jsonify({
        "base_scene": base_scene,
        "dialogue": base_dialogue,
        "cameos": cameos,
        "variants": variants
    })

@app.route("/ai_generate", methods=["POST"])
def ai_generate():
    if not AI_ENABLED:
        return jsonify({"error": "AI generation not available"}), 503
    
    try:
        system_prompt = """You are a creative prompt generator for SORA AI video generation.
Generate wild, surreal, cinematic prompts with a cyberpunk-bayou-noir aesthetic.
Mix absurd humor with cinematic visuals. Characters often include @obesewith.munky, @obesewith.glassy, @obesewith.yerm, @obesewith.teefred.
Think: swamp cyberpunk, neon gators, trap beats with frogs, cosmic loyalty tests, microwave negotiations.
Be weird, creative, and unexpected but keep it coherent enough to visualize."""

        user_prompt = """Generate 2 unique SORA video prompts. Each should include:
- scene: A bizarre but vivid scenario
- cameos: 1-4 character handles (use @obesewith.munky, @obesewith.glassy, @obesewith.yerm, @obesewith.teefred or make up new ones)
- camera: Creative camera movement description
- lighting: Atmospheric lighting description
- style: Visual style/aesthetic
- dialogue: One memorable quote from the scene
- sound: Audio/music description
- mood: Overall emotional vibe

Return JSON in this exact structure:
{
  "prompts": [
    {
      "model": "sora-2",
      "size": "1280x720",
      "seconds": 10,
      "prompt": {
        "scene": "...",
        "cameos": ["@character1", "@character2"],
        "camera": "...",
        "lighting": "...",
        "style": "...",
        "dialogue": "...",
        "sound": "...",
        "mood": "..."
      }
    },
    {
      "model": "sora-2",
      "size": "1280x720",
      "seconds": 11,
      "prompt": {
        "scene": "...",
        "cameos": ["@character3"],
        "camera": "...",
        "lighting": "...",
        "style": "...",
        "dialogue": "...",
        "sound": "...",
        "mood": "..."
      }
    }
  ]
}"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=1.2
        )
        
        result = json.loads(response.choices[0].message.content)
        
        if not isinstance(result, dict) or "prompts" not in result:
            return jsonify({"error": "Invalid response format from AI"}), 500
        
        prompts = result["prompts"]
        
        if not isinstance(prompts, list) or len(prompts) == 0:
            return jsonify({"error": "No prompts generated"}), 500
        
        return jsonify(prompts)
        
    except Exception as e:
        print(f"AI generation error: {e}")
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 500

@app.route("/remix", methods=["POST"])
def remix():
    data = request.get_json()
    video_link = data.get("video_link", "")
    original_prompt = data.get("original_prompt", "")
    characters = data.get("characters", "")
    style = data.get("style", "")
    lighting = data.get("lighting", "")
    camera = data.get("camera", "")
    music = data.get("music", "")
    mood = data.get("mood", "")
    
    char_list = [c.strip() for c in characters.split(",")] if characters else []
    
    remix_config = {
        "characters": char_list,
        "style": style or "original style",
        "lighting": lighting or "original lighting",
        "camera": camera or "original camera work",
        "music": music or "original soundtrack",
        "mood": mood or "original mood"
    }
    
    sora_prompt = f"Recreate the following scene with these modifications:\n\n"
    sora_prompt += f"ORIGINAL: {original_prompt}\n\n"
    sora_prompt += f"REMIX SETTINGS:\n"
    if char_list:
        sora_prompt += f"- Replace characters with: {', '.join(char_list)}\n"
    if style:
        sora_prompt += f"- Style: {style}\n"
    if lighting:
        sora_prompt += f"- Lighting: {lighting}\n"
    if camera:
        sora_prompt += f"- Camera: {camera}\n"
    if music:
        sora_prompt += f"- Music/Sound: {music}\n"
    if mood:
        sora_prompt += f"- Mood: {mood}\n"
    sora_prompt += f"\nKeep the core scene and pacing, but apply these creative treatments to make it fresh."
    
    return jsonify({
        "original_video": video_link,
        "remix_version": f"{char_list[0] if char_list else 'Unknown'} Cinematic Remix",
        "remix_config": remix_config,
        "sora_prompt": sora_prompt
    })

@app.route("/save_characters", methods=["POST"])
def save_characters():
    if not DB_ENABLED:
        return jsonify({"message": "Database temporarily unavailable - characters not saved", "saved": [], "skipped": []}), 200
    
    data = request.get_json()
    characters = data.get("characters", "")
    char_list = [c.strip() for c in characters.split(",") if c.strip()]
    
    if not char_list:
        return jsonify({"error": "No characters provided"}), 400
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"message": "Database temporarily unavailable - characters not saved", "saved": [], "skipped": []}), 200
            
        cur = conn.cursor()
        saved = []
        skipped = []
        
        for char in char_list:
            try:
                cur.execute("INSERT INTO custom_characters (character_name) VALUES (%s)", (char,))
                conn.commit()
                saved.append(char)
            except psycopg2.IntegrityError:
                conn.rollback()
                skipped.append(char)
        
        cur.close()
        conn.close()
        
        # Better messaging
        if len(saved) > 0 and len(skipped) > 0:
            message = f"✅ Saved {len(saved)} new character(s). ⚠️ {len(skipped)} already in database: {', '.join(skipped)}"
        elif len(saved) > 0:
            message = f"✅ Saved {len(saved)} character(s) successfully!"
        elif len(skipped) > 0:
            message = f"ℹ️ All {len(skipped)} character(s) already exist in database: {', '.join(skipped)}"
        else:
            message = "No characters processed."
        
        return jsonify({
            "saved": saved,
            "skipped": skipped,
            "message": message
        })
    except Exception as e:
        print(f"Error in save_characters: {e}")
        return jsonify({"message": "Database temporarily unavailable - characters not saved", "saved": [], "skipped": []}), 200

@app.route("/get_characters", methods=["GET"])
def get_characters():
    if not DB_ENABLED:
        # Return default saved characters when DB is unavailable
        default_chars = ["@obesewith.cookie", "@obesewith.teefred", "@obesewith.yerm", 
                        "@obesewith.jamarcus", "@obesewith.munky", "@obesewith.glassy"]
        return jsonify({"characters": default_chars})
    
    try:
        conn = get_db_connection()
        if not conn:
            # Return default chars if connection fails
            default_chars = ["@obesewith.cookie", "@obesewith.teefred", "@obesewith.yerm", 
                            "@obesewith.jamarcus", "@obesewith.munky", "@obesewith.glassy"]
            return jsonify({"characters": default_chars})
            
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT character_name, created_at FROM custom_characters ORDER BY created_at DESC")
        characters = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({"characters": [c["character_name"] for c in characters]})
    except Exception as e:
        print(f"Error in get_characters: {e}")
        # Return default chars on error
        default_chars = ["@obesewith.cookie", "@obesewith.teefred", "@obesewith.yerm", 
                        "@obesewith.jamarcus", "@obesewith.munky", "@obesewith.glassy"]
        return jsonify({"characters": default_chars})

@app.route("/snap_remix", methods=["POST"])
def snap_remix():
    """Generate Snap-style remix with Tyrone personality"""
    try:
        # Load the snap style configuration
        with open('snap_style_generator.json', 'r') as f:
            snap_data = json.load(f)
        
        # Get personality from request or default to random
        data = request.get_json() or {}
        personality = data.get("personality", random.choice(snap_data["personality_level"]))
        
        # Random selections from each category
        duration = random.choice(snap_data["video_duration_sec"])
        theme = random.choice(snap_data["theme"])
        lighting = random.choice(snap_data["lighting_style"])
        camera = random.choice(snap_data["camera_effects"])
        visual = random.choice(snap_data["visual_style"])
        audio = random.choice(snap_data["audio_style"])
        text_style = random.choice(snap_data["text_overlay_style"])
        cta = random.choice(snap_data["call_to_action"])
        
        # Get random scene and characters from existing banks
        scene = random.choice(scene_options)
        cameos = random.choice(cameos_options)
        
        # Add Tyrone-style flavor text based on personality
        if personality == "calm":
            vibe = "Relaxed and cinematic, smooth transitions and natural tone."
            narration_style = "chill and conversational"
        elif personality == "witty":
            vibe = "Playful rhythm, quick cuts, tongue-in-cheek narration, sharp one-liners."
            narration_style = "clever and sarcastic"
        else:  # unhinged
            vibe = "Chaotic and explosive, jump cuts, spinning shots, wild energy, unfiltered Tyrone commentary!"
            narration_style = "absolutely wild and unfiltered"
        
        # Build the Sora-ready prompt
        sora_prompt = f"""[SNAP REMIX - {personality.upper()} MODE]

🎬 Duration: {duration}s
🎨 Theme: {theme}
💡 Lighting: {lighting}
📹 Camera: {camera}
🎞️ Visual: {visual}
🎵 Audio: {audio}
📝 Text Style: {text_style}
🗣️ Personality: {personality.upper()}
👥 Characters: {', '.join(cameos)}

📍 SCENE:
{scene}

🎯 VIBE:
{vibe}

🎙️ TYRONE NARRATION ({narration_style}):
"Yo, it's {theme} energy time, baby! We got {', '.join(cameos)} in the mix! Let's roll the dice, snap the vibe, and flip the scene — {cta}!"

🔥 EXECUTION:
Create a fast-cut, {theme.lower()} inspired clip with {lighting.lower()} lighting and {camera.lower()} camera motion. 
Add {visual.lower()} visuals synced to {audio.lower()} soundtrack. 
On-screen text styled as {text_style.lower()} flashes across the screen with "{cta}".

⚡ CALL TO ACTION: {cta}"""
        
        return jsonify({
            "personality": personality,
            "duration": duration,
            "theme": theme,
            "characters": cameos,
            "scene": scene,
            "sora_prompt": sora_prompt.strip(),
            "config": {
                "lighting": lighting,
                "camera": camera,
                "visual": visual,
                "audio": audio,
                "text_style": text_style,
                "cta": cta
            }
        })
    except Exception as e:
        print(f"Error in snap_remix: {e}")
        return jsonify({"error": "Failed to generate snap remix"}), 500

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    filename = data.get("filename", "sora_prompts.json")
    notes = data.get("notes", "No notes provided.")
    creator_info = {
        "creator": "@obesewitherspooon",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "notes": notes
    }
    
    output = {
        "metadata": creator_info,
        "prompts": data.get("content", {})
    }
    
    json_str = json.dumps(output, indent=2)
    buffer = io.BytesIO()
    buffer.write(json_str.encode("utf-8"))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype="application/json")

@app.route("/generate", methods=["POST"])
def generate_video():
    """Generate video using updated Kie.AI API endpoints with fallback"""
    data = request.get_json()
    prompt = data.get("prompt")
    duration = data.get("duration", 10)
    resolution = data.get("resolution", "720p")
    api_key = data.get("api_key")  # Optional - can use env var
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Use provided API key or environment variable
    key_to_use = api_key or os.environ.get("KIE_API_KEY")
    
    if not key_to_use:
        return jsonify({"error": "API key required. Set KIE_API_KEY env var or provide in request"}), 400
    
    # Correct Kie.AI endpoint from latest documentation
    url = "https://api.kie.ai/v1/video/generations"
    
    # Correct payload structure according to latest docs
    payload = {
        "model": "sora-2-pro",
        "prompt": prompt,
        "resolution": resolution,
        "aspect_ratio": "16:9",
        "duration": int(duration),
        "remove_watermark": True  # Added for better quality
    }
    
    headers = {
        "Authorization": f"Bearer {key_to_use}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Calling Kie.AI API: {url}")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # Kie.AI returns a task_id for async processing
            return jsonify({
                "taskId": result.get("task_id"),
                "status": "queued",
                "message": "Video generation started. Use the taskId to check status."
            })
        elif response.status_code == 401:
            return jsonify({"error": "Invalid API key. Please check your Kie.AI API key."}), 401
        elif response.status_code == 429:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        elif response.status_code == 400:
            error_data = response.json() if response.text else {"error": "Invalid request parameters"}
            return jsonify(error_data), 400
        else:
            error_msg = f"API error: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", error_msg)
                except:
                    error_msg += f" - {response.text[:200]}"
            return jsonify({"error": error_msg}), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Video generation might take longer."}), 504
    except requests.exceptions.RequestException as e:
        print(f"Kie.AI API request error: {e}")
        return jsonify({"error": f"Connection error: {str(e)}"}), 503
    except Exception as e:
        print(f"Error in generate_video: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/check-status/<task_id>", methods=["GET"])
def check_status(task_id):
    """Check the status of a video generation task"""
    api_key = request.args.get("api_key") or os.environ.get("KIE_API_KEY")
    
    if not api_key:
        return jsonify({"error": "API key required"}), 400
    
    # Correct status check endpoint
    url = f"https://api.kie.ai/v1/video/generations/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "taskId": result.get("taskId"),
                "status": result.get("status"),
                "video_url": result.get("video_url"),
                "processing_time": result.get("processing_time"),
                "credits_used": result.get("credits_used")
            })
        else:
            return jsonify({"error": f"Failed to check status: {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sora-generate", methods=["POST"])
def sora_generate_kieai():
    """Generate video using Kie.AI Sora 2 Pro API"""
    try:
        data = request.get_json()
        api_key = data.get("api_key")
        prompt = data.get("prompt")
        duration = data.get("duration", 10)
        resolution = data.get("resolution", "720p")
        
        if not api_key:
            return jsonify({"error": "API key is required"}), 400
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Call Kie.AI Sora 2 Pro API
        response = requests.post(
            "https://api.kie.ai/v1/sora",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sora-2-pro",
                "prompt": prompt,
                "duration": duration,
                "resolution": resolution
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # Kie.AI might return a job ID for processing or direct URL
            if result.get("url"):
                return jsonify({
                    "status": "completed",
                    "url": result["url"],
                    "duration": duration,
                    "resolution": resolution
                })
            elif result.get("job_id"):
                return jsonify({
                    "status": "processing",
                    "job_id": result["job_id"],
                    "message": "Video is being generated. Check back in a few moments."
                })
            else:
                return jsonify(result)
        elif response.status_code == 401:
            return jsonify({"error": "Invalid API key"}), 401
        elif response.status_code == 429:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        else:
            error_data = response.json() if response.text else {"error": f"API error: {response.status_code}"}
            return jsonify(error_data), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Video generation might take longer."}), 504
    except requests.exceptions.RequestException as e:
        print(f"Kie.AI API request error: {e}")
        return jsonify({"error": f"Connection error: {str(e)}"}), 503
    except Exception as e:
        print(f"Error in sora_generate_kieai: {e}")
        return jsonify({"error": "Failed to generate video"}), 500

if __name__ == '__main__':
    # Run in production mode for stability - no debug, no reloader
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)