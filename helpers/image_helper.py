from PIL import Image
import webp

def convert_to_webp(input_image_path, output_image_path):
    try:
        image = Image.open(input_image_path)
        image.save(output_image_path, 'WEBP')
        print(f"Image converted successfully and saved as {output_image_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

def image_compression(image_path:str, width, height, stride, quality_factor):

    # Load an image
    with open('input_image.png', 'rb') as f:
        image_data = f.read()

    # Compress the image
    compressed_data = webp.WebPEncodeRGB(image_data, width, height, stride, quality_factor)

