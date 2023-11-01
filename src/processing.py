from PIL import Image 
from collections import defaultdict


def round_pixel_color(pixel: tuple, step: int=16) -> tuple:
    """This function is used to classify colors on a scale of 0 to 255 by the given step
    

    Args:
        pixel (tuple): tuple representing a pixel color in RGB (e.g. (0, 0, 0) for a black pixel)
        step (int, optional): int that should be given a base 10 number that represents an octet where only
            one bit has the value 1 to function as intended.
            A lower number will make the program run much slower. Defaults to 16.

    Returns:
        tuple: returns the rounded color, rounds color to the lower bound.
    """
    return (pixel[0] - pixel[0] % step, pixel[1] - pixel[1] % step, pixel[2] - pixel[2] % step)


def normalize_to_permille(color_list: list[tuple]) -> list[tuple]:
    """All of the pixels of the given image have been counted, 
    this function normalize them to permille and returns a list of tuple

    Args:
        color_list (list[tuple]): tuple(tuple, int) [0] representing the RGB color, [1] the number of occurence

    Returns:
        list[tuple]: tuple(tuple, int) [0] representing the RGB color, [1] the permille
    """
    total = sum(list(map(lambda val: val[1], color_list)))
    full = 0
    result = []
    for i in color_list:
        permille = (i[1] / total) * 1000
        if permille < 1:
            continue
        full += round(permille)

        result.append((i[0], round(permille)))

    return result


def create_color_palette_image(colors: list[tuple]):
    im = Image.new(mode="RGB", size=(1000, 1000))
    pixels = []
    start, end = 0, 0

    for color in colors:
        rgb_tuple, percentage = color
        size = round(percentage) * 1000
        end += size

        pixels[start: end] = [rgb_tuple] * size
        start = end + 1

    im.putdata(pixels)

    im.save("src\out\color_palette.jpg")

    

with Image.open("src\img\knowyourself.jpg", "r") as img:
    print(img)
    pix_val = list(img.getdata())

    colors_counted = defaultdict(int)
    for i in pix_val:
        rounded_pixel = round_pixel_color(i)

        if colors_counted.get(rounded_pixel):
            colors_counted[rounded_pixel] += 1
            continue
        colors_counted[rounded_pixel] = 1

    
    result = sorted(colors_counted.items(), key=lambda item:item[1], reverse=True)
    
    normalized_result = normalize_to_permille(result)

    create_color_palette_image(normalized_result)

