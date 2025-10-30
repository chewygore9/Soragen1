from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

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
    "\"You ever seen smoke argue back? That's when I knew I was chosen.\"",
    "\"Down here, loyalty's like gator teeth — sharp till it breaks.\"",
    "\"I ain't paranoid if they really cloning me.\"",
    "\"Sometimes I dream in 480p, bro.\"",
    "\"Munky, stop touching buttons you don't understand!\"",
    "\"If it's glowing, that means it's money… or radiation.\"",
    "\"This swamp got more secrets than my search history.\"",
    "\"They told me I couldn't be two things at once — so I became three.\""
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
