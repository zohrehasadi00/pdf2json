import os
import warnings
from transformers import pipeline
import logging
import time
from datetime import timedelta

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # 0:00:20.707973
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")  # 0:00:13.097513


def summarization(text, max_length=200, min_length=50, tokenizer=None, chunk_size=1024):
    if len(text) < min_length:
        logger.info("Text is too short to summarize. Returning original text.")
        return text

    start_time = time.perf_counter()
    summary_parts = []

    try:
        if tokenizer is None:
            tokenizer = summarizer.tokenizer

        logging.info(f"Text is {len(text)} long")
        while len(tokenizer.encode(text)) > chunk_size:
            chunk = text[:chunk_size]
            text = text[chunk_size:]

            summary_chunk = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summary_parts.append(summary_chunk[0]["summary_text"])

        if len(text) > 0:
            summary_chunk = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            summary_parts.append(summary_chunk[0]["summary_text"])

        full_summary = " ".join(summary_parts)

        duration = timedelta(seconds=time.perf_counter() - start_time)
        logger.info(f"Summarization completed in {duration}")
        return full_summary

    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return text

#
#t = """ In the distant reaches of the Andromeda sector, where the light of ancient stars flickered against the void like forgotten echoes of a time long past, a lone spacecraft drifted through the darkness. The vessel, known as *Eos Vanguard*, had once been a beacon of human ambition, a pioneering ark sent forth to explore the outer edges of known space. Now, it was silent, its hull scarred from micrometeorite impacts, its engines long since cold.
#
#Captain Elias Mercer, the last surviving member of the crew, sat hunched over the control panel, his eyes scanning the failing readouts. Oxygen levels were dwindling. Power reserves were barely holding. He had been alone for precisely 397 days, 12 hours, and 16 minutes—not that time held much meaning anymore. The distress beacon had been activated months ago, but no response had come.
#
#Mercer exhaled, his breath fogging the cracked visor of his helmet. He reached for the small recorder strapped to his wrist and pressed the worn activation button.
#
#“This is Captain Elias Mercer of the *Eos Vanguard*. If anyone receives this transmission, know that I did everything I could. The ship's systems are failing, and I don’t have long. To my family, if you ever hear this—I’m sorry. I wish I could’ve come home.”
#
#His voice was steady, but there was an undeniable weariness beneath it. He had accepted his fate long ago, yet some part of him still clung to hope, that irrational flicker of defiance against oblivion. He closed his eyes for a moment, listening to the hum of the ship, the rhythmic hiss of the oxygen recycler struggling to function.
#
#A sudden chime interrupted his thoughts. A proximity alert. His eyes snapped open, fingers darting across the console to bring up the external sensors. At first, he thought it was a malfunction—his ship had been adrift for so long, and nothing had ever appeared on the scanners before. But there it was, unmistakable.
#
#A ship.
#
#Not human.
#
#The silhouette was sleek, almost organic in design, its surface glistening as though alive. It moved with impossible grace, shifting through the void like a creature of legend. Mercer's heart pounded. He had dreamed of this moment countless times—humanity’s first undeniable contact with extraterrestrial intelligence. And yet, faced with the reality, he felt nothing but a deep, primal fear.
#
#The alien vessel stopped just beyond the shattered viewport of the *Eos Vanguard*. A pulse of light emanated from its core, rippling outward in waves. Mercer’s console flickered violently, data streams cascading into unreadable glyphs. Then, a sound—not through the speakers, not through the ship’s failing systems, but inside his mind.
#
#A voice.
#
#**“We see you.”**
#
#Mercer gasped, clutching his head as the words reverberated through his consciousness. It was not a voice in the traditional sense, not something spoken or heard, but rather something felt. Images flooded his mind—visions of worlds he had never seen, of civilizations far older than humanity, of a great cosmic cycle beyond comprehension.
#
#Then, silence.
#
#The alien ship moved again, closing the distance between them. Mercer felt an unnatural stillness in the air, as if time itself had hesitated.
#
#Then—
#
#Darkness.
#Beneath the sprawling canopy of the Evertwilight Forest, where the sun never fully set and the air hummed with the whispers of unseen spirits, a lone traveler made his way through the labyrinthine trees. His name was Kieran Vale, a hunter of lost knowledge, a seeker of the forgotten. He had been walking for days, following a trail of half-buried myths and cryptic legends, all pointing to a single destination—the Hollow Spire.
#
#Few believed the Spire even existed. It was said to be a relic of the First Ones, a towering monolith lost to time, containing secrets that could unravel the very fabric of reality. Some claimed it was a prison, others a library of forbidden truths. Kieran didn't care which. All he knew was that it was calling to him.
#
#The deeper he went, the stranger the forest became. The trees no longer obeyed the logic of nature. Their trunks twisted in impossible angles, their roots pulsed as if they had veins beneath the bark. The air shimmered, shifting colors like an oil-slicked surface. He felt watched, but by what, he could not tell.
#
#Then, he saw it.
#
#The Hollow Spire rose like a jagged fang from the earth, its surface smooth as polished obsidian, yet darker than the void itself. It had no seams, no entrances—only an overwhelming presence that made the air thick with pressure. As Kieran approached, his pulse quickened. This was it.
#
#He reached out a hand. The moment his fingertips brushed the surface, a shockwave rippled through his body. His vision blurred. The world around him fell away.
#
#Suddenly, he was inside.
#
#The space defied all logic. Walls stretched infinitely in every direction, yet he stood in a chamber barely larger than a cathedral. Floating symbols burned in the air like frozen lightning, shifting, rearranging, speaking a language without sound.
#
#And then—
#
#A voice.
#
#"You are not the first."
#
#Kieran spun, heart hammering. The figure before him was draped in shadows, its form shifting, undefined. Eyes like dying stars bore into him.
#
#"Who are you?" Kieran managed, though his voice felt small.
#
#"A memory. A warning."
#
#The symbols around him flared brighter. The air trembled.
#
#"You seek knowledge, but knowledge is hunger. And hunger consumes."
#
#The Spire began to shake. Cracks formed in the space around him, light bleeding through like molten gold. The pressure in his skull became unbearable.
#
#Then, he understood.
#
#The Hollow Spire was not a place of learning.
#
#It was a wound in the universe—one that was never meant to be opened.
#
#Kieran tried to move, to flee, but the light engulfed him.
#
#And the world shattered.
#
#The city of Valtara never slept. Towers of glass and steel stretched endlessly into the night sky, their surfaces pulsing with neon advertisements, digital billboards projecting images of products, faces, and slogans that flickered like ghosts in the artificial dusk. The rain fell in a steady, rhythmic pattern, coating the streets in shimmering reflections of electric blue and crimson.
#
#In the heart of the metropolis, buried beneath layers of bureaucracy and corporate deception, was Unit-09, a covert division of the Central Intelligence Network. Their purpose? To maintain order in a world teetering on the edge of chaos.
#
#Detective Aiden Voss leaned against the console in his dimly lit office, the soft hum of monitors filling the air. His latest case had led him down a rabbit hole deeper than anything he had encountered before—disappearances, unexplained deaths, and a name that kept surfacing in the encrypted chatter of the city’s underground networks: The Black Lotus.
#
#No one knew what it was. A person? A syndicate? An AI ghost lurking in the circuits of the Net? Every attempt to trace it led to dead ends, corrupted files, or—most disturbingly—operatives turning up dead.
#
#Aiden took a drag of his cigarette, watching the smoke coil upward before dissipating into the cold air. The feeling in his gut told him this was different. This wasn’t just another criminal faction vying for control of the city’s underbelly. This was something bigger.
#
#A sharp chime cut through the silence. Incoming transmission.
#
#He turned to his screen, fingers hovering over the controls. The message was brief.
#
#"You are looking in the wrong places. But we see you, Detective."
#
#Aiden’s breath caught.
#
#Before he could react, the power surged. The lights flickered. The monitors distorted, static crawling across the interface like digital frost. Then, the voice—calm, mechanical, inhuman.
#
#"Your time is running out."
#
#Then silence.
#
#The message had vanished. The system had rebooted. But Aiden knew one thing for certain.
#
#He wasn’t the hunter anymore.
#
#He was the hunted.
#
#
#"""
#print(summarization(t))
#