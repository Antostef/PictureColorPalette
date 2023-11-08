from PIL import Image 
from collections import defaultdict

letters_and_numbers = {
    "r": ["00000000 ","01111110 ","011111110","011000110","0110 0110","011000110","01111110 ","01111110 ","011000110","0110 0110","0110 0110","0110 0110","0110 0110","0000 0000"],
    "g": [" 0000000 ","001111100","011111110","011000000","0110     ","01100000 ","011001100","011001110","011000110","0110 0110","011000110","011111110","001111100"," 0000000 "],
    "b": ["00000000 ","011111100","011111110","011000110","0110 0110","011000110","011111100","011111100","011000110","0110 0110","011000110","011111110","011111100","00000000 "],
    "1": ["000000000","022222110","022222110","022000110","0220 0110","022000110","022222110","022222110","022000110","0220 0110","022000110","022222110","022222110","000000000"],
    "2": ["000000000","021111120","011111110","022000110","0220 0110","022000110","021111110","011111120","011000220","0110 0220","011000220","011111110","011111110","000000000"],
    "3": ["000000000","011111120","011111110","022000110","0220 0110","022000110","011111110","011111110","022000110","0220 0110","022000110","011111110","011111120","000000000"],
    "4": ["000000000","011222110","011222110","011000110","0110 0110","011000110","011111110","011111110","022000110","0220 0110","022000110","022222110","022222110","000000000"],
    "5": ["000000000","011111110","011111110","011000220","0110 0220","011000220","011111120","011111110","022000110","0220 0110","022000110","011111110","011111120","000000000"],
    "6": ["000000000","011222220","011222220","011000220","0110 0220","011000220","011111120","011111110","011000110","0110 0110","011000110","011111110","021111120","000000000"],
    "7": ["000000000","011111110","011111110","022000110","0220 0110","022000110","022222110","022222110","022000110","0220 0110","022000110","022222110","022222110","000000000"],
    "8": ["000000000","021111120","011111110","011000110","0110 0110","011000110","021111120","021111120","011000110","0110 0110","011000110","011111110","021111120","000000000"],
    "9": ["000000000","021111120","011111110","011000110","0110 0110","011000110","011111110","021111110","022000110","0220 0110","022000110","022222110","022222110","000000000"],
    "0": ["000000000","021111120","011111110","011000110","0110 0110","011000110","011222110","011222110","011000110","0110 0110","011000110","011111110","021111120","000000000"]
}


def create_letter_print(color: tuple) -> str:
    result = "rgb"

    for i in color:
        if i == 0:
            result+= "000"
            continue
        result += str(i)
    
    return result


def add_rgb_on_color_band(color_band: list[tuple]) -> list[tuple]:
    white, black, grey = (0, 0, 0), (255, 255, 255), (192, 192, 192)
    line, column = 7, 11
    letter_height = len(letters_and_numbers.get("r"))
    letter_width = len(letters_and_numbers.get("r")[0])
    letter_print = create_letter_print(color_band[0])

    if len(color_band) / 1000 > letter_height*2: 
        for i in range(len(letter_print)):
            for j in letters_and_numbers.get(letter_print[i]):
                for k in j:
                    try:
                        if int(k) == 1:
                            color_band[line*1000 + column] = white
                        elif int(k) == 2:
                            color_band[line*1000 + column] = grey
                        else:
                            color_band[line*1000 + column] = black
                    except:
                        pass
                    finally:
                        column += 1
                line += 1

                column -= len(j)
            spaces = 3
            if (i+1) % 3 == 0:
                spaces += 3

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
        pixels[start: end] = add_rgb_on_color_band([rgb_tuple] * size)
        start = end + 1

    im.putdata(pixels)

    im.save("src\out\color_palette.jpg")

    
with Image.open("src\img\knowyourself.jpg", "r") as img:
    pix_val = list(img.getdata())

    colors_counted = defaultdict(int)
    for i in pix_val:
        rounded_pixel = round_pixel_color(i)

        if colors_counted.get(rounded_pixel):
            colors_counted[rounded_pixel] += 1
            continue
        colors_counted[rounded_pixel] = 1

    
    result = sorted(colors_counted.items(), key=lambda item:item[1], reverse=True)
    
    normalized_result = normalize_to_permille(result[:5])

    create_color_palette_image(normalized_result)

