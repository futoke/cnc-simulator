def generate(*colors, grad_len=256):
    """The function to generate the gradient and returns the list of colors as
    packed color strings.
    """

    colors_per_step = grad_len / len (colors)
    # Get the 'corrected' length of the gradient...
    num_colors = int(colors_per_step) * len(colors)

    # Color conversion utils.
    f2c = lambda f: int(f * 255.0) & 0xff
    c2f = lambda c: float(c) / 255.0
    red = lambda c: (c >> 16) & 0xff
    green = lambda c: (c >> 8) & 0xff
    blue = lambda c: c & 0xff
    pack = lambda r, g, b: ((f2c(r) << 16) | (f2c(g) << 8) | f2c(b))

    gradient = []

    for i, color in enumerate(colors):
        # start color...
        r1 = c2f(red(color))
        g1 = c2f(green(color))
        b1 = c2f(blue(color))

        # end color...
        color2 = colors[(i + 1) % len(colors)]
        r2 = c2f(red(color2))
        g2 = c2f(green(color2))
        b2 = c2f(blue(color2))

        # generate a gradient of one step from color to color:
        delta = 1.0 / colors_per_step
        for j in range(int(colors_per_step)):
            t = j * delta
            r = (1.0 - t) * r1 + t * r2
            g = (1.0 - t) * g1 + t * g2
            b = (1.0 - t) * b1 + t * b2
            gradient.append('#{0:x}'.format(pack(r, g, b)))

    return gradient


if __name__ == '__main__':
    print(generate(0x00ff00, 0xff0000))
