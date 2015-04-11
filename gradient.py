def hex_to_RGB(hx):
    ''' "#FFFFFF" -> [255,255,255] '''

    # Pass 16 to the integer function for change of base.
    return [int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''

    # Components need to be integers for hex to make sense.
    RGB = [int(x) for x in RGB]
    return "#" + "".join(
        ["0{0:x}".format(v) if v < 16 else"{0:x}".format(v) for v in RGB]
    )


def generate(start_hex, finish_hex="#FFFFFF", n=40):
    '''Returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF")
    '''
    
    # Initilize a list of the output colors with the starting color.
    RGB_list = [start_hex]

    # Starting and ending colors in RGB form.
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    
    # Calcuate a color at each evenly spaced value of t from 1 to n.
    for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t.
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(RGB_to_hex(curr_vector))

    return RGB_list


if __name__ == '__main__':
    
    gradient = generate('#00ff00', '#ff0000')
    for color in gradient:
        print(color)
