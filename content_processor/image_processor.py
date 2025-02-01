from transformers import CLIPProcessor, CLIPModel, pipeline
from PIL import Image
import torch

# Load models
clip_model=CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor=CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
summarizer=pipeline("summarization",model="facebook/bart-large-cnn")

def check_relevance(image:Image,text:str)->float:
    inputs=clip_processor(text=[text],images=image,return_tensors="pt",padding=True)
    with torch.no_grad():
        outputs=clip_model(**inputs)
    return outputs.logits_per_image.item() # Higher means more relevant