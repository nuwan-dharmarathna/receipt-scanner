# import torch
# from PIL import Image
# from donut import DonutModel
# import warnings
# warnings.filterwarnings("ignore", category=UserWarning)

# # Load pre-trained Donut model for receipt OCR
# MODEL_NAME = "naver-clova-ix/donut-base-finetuned-cord-v2"
# TASK_PROMPT = "<s_cord-v2>"

# class OCRModel:
#     def __init__(self):
#         self.model = DonutModel.from_pretrained(MODEL_NAME)
#         self.model.eval()
        
#     def extract_text(self, image: Image.Image):
#         """Processes the receipt image and returns structured text."""
#         result = self.model.inference(image=image, prompt=TASK_PROMPT)["predictions"][0]
#         return result
    
# # Initialize and keep the model loaded
# ocr_model = OCRModel()