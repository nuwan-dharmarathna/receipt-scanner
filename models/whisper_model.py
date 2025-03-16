from transformers import pipeline

# load the whisper model
whisper_model = pipeline("automatic-speech-recognition", model="openai/whisper-medium", device=-1)

