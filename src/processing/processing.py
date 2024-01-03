from os import remove, path
from PIL import Image 
from collections import defaultdict

letters_and_numbers = {
    "r": ["00000000 ","011111100","011111110","011000110","0110 0110","011000110","011111100","011111100","011000110","0110 0110","0110 0110","0110 0110","0110 0110","0000 0000"],
    "g": [" 0000000 ","001111100","011111110","011000000","0110     ","01100000 ","011001100","011001110","011000110","0110 0110","011000110","011111110","001111100"," 0000000 "],
    "b": ["00000000 ","011111100","011111110","011000110","0110 0110","011000110","011111100","011111100","011000110","0110 0110","011000110","011111110","011111100","00000000 "],
    "1": ["     0000","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0000"],
    "2": [" 0000000 ","001111100","011111110","000000110","     0110"," 00000110","001111110","011111100","01100000 ","0110     ","011000000","011111110","011111110","000000000"],
    "3": ["00000000 ","011111100","011111110","000000110","     0110"," 00000110"," 01111110"," 01111110"," 00000110","     0110","000000110","011111110","011111100","00000000 "],
    "4": ["0000 0000","0110 0110","0110 0110","0110 0110","0110 0110","011000110","011111110","011111110","000000110","     0110","     0110","     0110","     0110","     0000"],
    "5": ["000000000","011111110","011111110","011000000","0110     ","01100000 ","011111100","011111110","000000110","     0110","000000110","011111110","011111100","00000000 "],
    "6": ["0000     ","0110     ","0110     ","0110     ","0110     ","01100000 ","011111100","011111110","011000110","0110 0110","011000110","011111110","001111100"," 0000000 "],
    "7": ["000000000","011111110","011111110","000000110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0110","     0000"],
    "8": [" 0000000 ","001111100","011111110","011000110","0110 0110","011000110","001111100","001111100","011000110","0110 0110","011000110","011111110","001111100"," 0000000 "],
    "9": [" 0000000 ","001111100","011111110","011000110","0110 0110","011000110","011111110","001111110"," 00000110","     0110","     0110","     0110","     0110","     0000"],
    "0": [" 0000000 ","001111100","011111110","011000110","0110 0110","0110 0110","0110 0110","0110 0110","0110 0110","0110 0110","011000110","011111110","001111100"," 0000000 "]
}


def create_letter_print(color: tuple) -> str:
    """Create a string from the given color

    Args:
        color (tuple): RGB color given as a tuple

    Returns:
        str: rgb + each numerical color value (e.g. "RGB 123 045 789")
    """
    result = "rgb"

    for i in color:
        while len(str(i)) < 3:
            i = "0" + str(i)
        result += str(i)
    
    return result


def add_rgb_on_color_band(color_band: list[tuple], width_height) -> list[tuple]:
    """creates a tag representing the rgb color used for the current band

    Args:
        color_band (list[tuple]): list of color tuples on which the tag is added

    Returns:
        list[tuple]: color band with rgb color tag on it
    """
    white, black, grey = (0, 0, 0), (255, 255, 255), (192, 192, 192)
    line, column = 7, 11
    letter_height = len(letters_and_numbers.get("r"))
    letter_width = len(letters_and_numbers.get("r")[0])
    letter_print = create_letter_print(color_band[0])

    if len(color_band) / width_height > letter_height*2: 
        for i in range(len(letter_print)):
            for j in letters_and_numbers.get(letter_print[i]):
                for k in j:
                    try:
                        if int(k) == 1:
                            color_band[line*width_height + column] = white
                        elif int(k) == 2:
                            color_band[line*width_height + column] = grey
                        else:
                            color_band[line*width_height + column] = black
                    except:
                        pass
                    finally:
                        column += 1
                line += 1
                column -= len(j)
            spaces = 3
            if (i+1) % 3 == 0:
                spaces += 6

            line = int(letter_height/2)
            column += letter_width + spaces
    return color_band 


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


def normalize(color_list: list[tuple], per: int, rounding: int) -> list[tuple]:
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
        tmp = (i[1] / total) * per
        if tmp < 1:
            continue
        full += round(tmp)

        result.append((i[0], round(tmp, rounding)))

    return result


def create_color_palette_image(colors: list[tuple]):
    wh = 500
    im = Image.new(mode="RGB", size=(wh, wh))
    pixels = []
    start, end = 0, 0

    for color in colors:
        rgb_tuple, percentage = color
        size = round(percentage) * wh
        end += size
        pixels[start: end] = add_rgb_on_color_band([rgb_tuple] * size, wh)
        start = end + 1

    im.putdata(pixels)

    im.save("src\out\color_palette.png", bitmap_format="png")


def folder_cleanup():
    """
    Cleans the output folder of all possibly created files.
    """

    try:
        if path.exists("src\out\color_palette.csv"):
            remove(dir_fd="src\out\*")
        if path.exists("src\out\color_palette.png"):
            remove("src\out\color_palette.png")
        if path.exists("src\out\color_palette.jpg"):
            remove("src\out\color_palette.jpg")
    except:
        pass


def write_titles() -> str:
    return "rgb_color;percentage;\n"


def create_color_palette_file(colors: list[tuple]):
    with open("src\out\color_palette.csv", "a") as f:
        f.write(write_titles())
        for color in colors:
            f.write(f"{color[0]};{color[1]}\n")


def get_colors_from_picture(url: str = "", number_of_colors: int = 5):
    folder_cleanup()
    with Image.open(url, "r") as img:
        pix_val = list(img.getdata())

        colors_counted = defaultdict(int)
        for i in pix_val:
            rounded_pixel = round_pixel_color(i)

            if colors_counted.get(rounded_pixel):
                colors_counted[rounded_pixel] += 1
                continue
            colors_counted[rounded_pixel] = 1

        sorted_colors_by_count = sorted(colors_counted.items(), key=lambda item:item[1], reverse=True)

        if number_of_colors > 5:
            if number_of_colors > len(sorted_colors_by_count):
                create_color_palette_file(normalize(sorted_colors_by_count, 100, 2))
            create_color_palette_file(normalize(sorted_colors_by_count[:number_of_colors], 100, 2))
        else:
            create_color_palette_image(normalize(sorted_colors_by_count[:number_of_colors], 500, 0))
