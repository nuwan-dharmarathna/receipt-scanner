from google.cloud import translate_v2 as translate

trans_client = translate.Client.from_service_account_json("gcp_key.json")
