def create_text(info_dict) -> str:
    """
    specific to my use-case
    """
    infos = info_dict["info"]
    location = infos["location"]
    year = infos["year"]
    gender = "MEN" if infos["gender"] == "m" else "WOMEN"
    distance = infos["distance"]
    wetsuit = infos["wetsuit"]
    progress = infos["progress"]

    text = f" - {location} {year} - {gender.upper()} - {distance}m\n{progress}"
    if infos["descriptions"] is not None:
        if (info_dict["url"] == "https://youtu.be/asUQlc3Ic98") and (
            len(infos["descriptions"]) > 5
        ):
            # todo: a bit hacky
            print("no breaking line for 2024_toulouse_w_2")
        else:
            text += "\n"

        for desc in infos["descriptions"]:
            if (desc is None) or (len(desc) == 0):
                text += "\n"
            else:
                text += f"\n{'  ' + desc}" if desc[0] == " " else f"\n{'• ' + desc}"
    return text


def calculate_text_dimensions(overlay_text, fontsize):
    # Count the number of lines in the text
    n_lines = overlay_text.count("\n") + 1

    # Calculate approximate text height (each line is about 'fontsize' tall)
    text_height = n_lines * fontsize

    # Estimate text width (since it's a monospace font, it's much easier)
    max_line_length = max(len(line) for line in overlay_text.split("\n"))
    text_width = max_line_length * fontsize  # Monospace fonts make this simple

    # todo: use monospace
    text_width *= 0.6  # no need if monospace

    return text_width, text_height


def get_text_position(
    placement: str, width, height, text_width, text_height, margin_pix: int = 30
):
    """Map placement string to FFmpeg x and y coordinates."""

    if placement == "top_left":
        return margin_pix, margin_pix  # ...px from top-left corner
    elif placement == "top_middle":
        return (
            width - text_width
        ) / 2, margin_pix  # Centered horizontally, ...px from top
    elif placement == "top_right":
        return (
            width - text_width - margin_pix,
            margin_pix,
        )  # ...px from top-right corner
    elif placement == "center_left":
        return (
            margin_pix,
            (height - text_height) / 2,
        )  # Centered vertically, ...px from left
    elif placement == "center_middle":
        return (width - text_width) / 2, (
            height - text_height
        ) / 2  # Centered both ways
    elif placement == "center_right":
        return (
            width - text_width - margin_pix,
            (height - text_height) / 2,
        )  # Centered vertically, ...px from right
    elif placement == "bottom_left":
        return (
            margin_pix,
            height - text_height - margin_pix,
        )  # ...px from bottom-left corner
    elif placement == "bottom_middle":
        return (
            width - text_width
        ) / 2, height - text_height - margin_pix  # Centered horizontally, ...px from bottom
    elif placement == "bottom_right":
        return (
            width - text_width - margin_pix,
            height - text_height - margin_pix,
        )  # ...px from bottom-right corner
    else:
        # Default: top-left if placement is undefined or not recognized
        return margin_pix, margin_pix
