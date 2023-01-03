import io
import telegram
import wave
from telegram.ext import Updater, MessageHandler, Filters
import subprocess
from datetime import datetime
import time
import pygame

# Insert the token of the telegram bot.
TOKEN = ''

# Set up the Telegram bot
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher


# Define the audio queue
audio_queue = []

print("Megaphone ready! Send your voice messages to the bot and them will be played in this computer!")

# Define the function that will handle voice messages
def voice_message_handler(update, context):

    # Get the voice file from the message
    voice_file = update.message.voice.get_file()

    # Download the voice file
    current_time = datetime.now()
    current_time_string = str(current_time.day)+str(current_time.month)+str(current_time.hour)+str(current_time.minute)+str(current_time.second)
    voice_file.download(f'recordings/voice{current_time_string}.mp3')

    # Convert the file in wave
    subprocess.run(["ffmpeg", "-i", f'recordings/voice{current_time_string}.mp3', f'recordings/voice{current_time_string}.wav'])
    
    # Open the voice file as a wave file
    voice_wave = wave.open(f'recordings/voice{current_time_string}.wav') 

    # Add the voice file to the queue
    audio_queue.append([voice_wave, f'recordings/voice{current_time_string}.wav'])

# Add the message handler to the dispatcher
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message_handler))

# Start the bot
updater.start_polling()

# Start playing the audio queue
while True:
    if len(audio_queue) > 0:
        
        # Get the next audio file from the queue
        audio_tuple = audio_queue.pop(0)
        audio = audio_tuple[0]

        # Set up the audio stream
        audio_stream = audio.readframes(audio.getnframes())
        audio_channels = audio.getnchannels()
        audio_rate = int(audio.getframerate())
        audio_width = audio.getsampwidth()
        audio_format = ''.join([f'<', 'h' if audio_width == 2 else 'i', str(audio_width)])
        # Play the audio file
        # audio_stream.close()
        # audio_stream = wave.open('output.wav')

        pygame.mixer.init(48000,0,audio_channels)
        pygame.mixer.music.load(audio_tuple[1])
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass