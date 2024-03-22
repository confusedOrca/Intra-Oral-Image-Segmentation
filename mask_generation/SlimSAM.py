from transformers import SamModel, SamProcessor

model = SamModel.from_pretrained("Zigeng/SlimSAM-uniform-50")
processor = SamProcessor.from_pretrained("Zigeng/SlimSAM-uniform-50")