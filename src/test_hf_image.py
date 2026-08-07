import os

from huggingface_hub import InferenceClient


client = InferenceClient(api_key=os.environ["HF_TOKEN"])

prompt = """
Ultra realistic Lord Ganesha seated on a golden lotus inside an ancient
South Indian temple at sunrise, divine golden rays, cinematic volumetric
lighting, intricate crown and ornaments, peaceful sacred atmosphere,
highly detailed devotional artwork, vertical 9:16, no text, no watermark
"""

image = client.text_to_image(
    prompt=prompt,
    model="black-forest-labs/FLUX.1-schnell",
)

image.save("ganesha_test.png")

print("SUCCESS: ganesha_test.png generated")
