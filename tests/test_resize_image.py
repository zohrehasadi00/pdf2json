from PIL import Image
from io import BytesIO
from gui import resize_image

def test_resize_image_preserves_aspect_ratio():
    # Create dummy image
    original = Image.new('RGB', (1000, 500), color='white')

    # Save to buffer
    buffer = BytesIO()
    original.save(buffer, format='PNG')
    buffer.seek(0)

    # Resize: gets raw image bytes
    resized_bytes = resize_image(buffer, 500, 250)

    # Convert bytes back to an image for testing
    resized_img = Image.open(BytesIO(resized_bytes))

    assert resized_img.width == 500
    assert resized_img.height == 250
