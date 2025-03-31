from PIL import Image, ImageFilter, ImageEnhance


def preprocess_image(image: Image.Image) -> Image.Image:

    image = image.convert('L')  # Convert to grayscale

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)  # Increase contrast by a factor of 3

    image = image.point(lambda p: p > 128 and 255)   # Convert to black & white
    image = image.filter(ImageFilter.MedianFilter(3))   # Apply a blur filter to remove noise (replacing each pixel with the median of the surrounding 3*3 pixels)

    return image


"""
L: Luminance -> grey scale
0: pure black
255: pure white
128:  mid grey

"""