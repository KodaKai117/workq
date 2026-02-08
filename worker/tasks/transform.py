from PIL import Image

def process_image(job):
    img = Image.open(job["input_path"])
    img = img.resize((256, 256))
    img = img.convert("L")
    img.save(job["output_path"])