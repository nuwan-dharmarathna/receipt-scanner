from google.cloud import speech_v1 as speech

speech_client = speech.SpeechClient.from_service_account_file("gcp_key.json")