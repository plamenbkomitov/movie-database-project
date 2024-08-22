import requests
from io import BytesIO
from PIL import Image, ImageEnhance
from colors import color


def get_movie_cover_from_url(url):
    """
    Fetch an image from the specified URL and render it in ASCII format.

    Args:
        url (str): The URL of the image to be fetched.

    Returns:
        str: The ASCII representation of the image if successful, otherwise None.
    """

    response = requests.get(url)

    if response.status_code == 200:
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        return render(image)
    else:
        return None


def render(image, width=120, height_scale=0.55, colorize=True):
    """
    Convert an image to an ASCII representation with optional ANSI colors.

    Args:
        image (PIL.Image.Image): The image to be converted.
        width (int, optional): The output width in characters. Defaults to 120.
        height_scale (float, optional): The scale factor for the height. Defaults to 0.55.
        colorize (bool, optional): Whether to use ANSI colors. Defaults to True.

    Returns:
        str: The ASCII representation of the image.
    """

    org_width, orig_height = image.size
    aspect_ratio = orig_height / org_width
    new_height = aspect_ratio * width * height_scale
    image = image.resize((width, int(new_height)))
    image = image.convert('RGBA')
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    pixels = image.getdata()

    def mapto(r, g, b, alpha):
        if alpha == 0.:
            return ' '
        chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ".", " "]
        pixel = (r * 19595 + g * 38470 + b * 7471 + 0x8000) >> 16
        if colorize:
            return color(chars[pixel // 25], (r, g, b))
        else:
            return chars[pixel // 25]

    new_pixels = [mapto(r, g, b, alpha) for r, g, b, alpha in pixels]
    new_pixels_count = len(new_pixels)
    ascii_image = [''.join(new_pixels[index:index + width]) for index in range(0, new_pixels_count, width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image
