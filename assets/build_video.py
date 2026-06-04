from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, ColorClip
from moviepy.video.fx import Resize

IMG = r'C:\Users\opc\source\repos\recyclebin-website\assets\beach_lady_smile.png'
AUDIO = r'C:\Users\opc\AppData\Local\hermes\audio_cache\tts_20260604_060819.mp3'
OUT = r'C:\Users\opc\source\repos\recyclebin-website\assets\beach_lady_smile.mp4'

img = ImageClip(IMG)
audio = AudioFileClip(AUDIO)

img = img.with_duration(audio.duration)
img = img.with_start(0)
img = img.with_audio(audio)

w, h = 1920, 1080
title = TextClip.text(
    'A Lady Smiles Near the Beach',
    fontsize=72,
    color='white',
    font='Arial-Bold',
    size=(w - 120, None),
    method='caption',
    align='center',
)
title = title.with_position('center').with_duration(audio.duration)
title = title.with_start(0)
# fade in/out
title = title.with_opacity(
    lambda t: 0 if t <= 0 else (1.0 if t < 1 else (0 if t > audio.duration - 1 else (audio.duration - t)))
)

clip = CompositeVideoClip([img, title], size=(w, h))
clip.write_videofile(OUT, fps=30, codec='libx264', audio_codec='aac', threads=2)

