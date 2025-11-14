import base64

import pytest

from sutton_signwriting_font.swu import (
    swu_column_png,
    swu_column_svg,
    swu_columns_png,
    swu_columns_svg,
    swu_sign_normalize,
    swu_sign_png,
    swu_sign_svg,
    swu_symbol_normalize,
    swu_symbol_png,
    swu_symbol_svg,
)

# -------------------------
# Symbol normalization
# -------------------------


@pytest.mark.parametrize(
    "swu_sym, expected",
    [
        ("񀀁", "񀀁𝣾𝣷"),
        ("񀀁𝤆𝤆", "񀀁𝣾𝣷"),
        ("񀀁𝤆𝤆-C", "񀀁𝣾𝣷-C"),
    ],
)
def test_swu_symbol_normalize(swu_sym, expected):
    norm = swu_symbol_normalize(swu_sym)
    assert norm == expected


def test_swu_symbol_normalize_invalid():
    norm = swu_symbol_normalize("񆉀")
    assert norm == ""


# -------------------------
# Symbol SVG
# -------------------------


@pytest.mark.parametrize(
    "swu_sym, expected",
    [
        (
            "񀀁",
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="16" height="30" viewBox="492 485 16 30">\n'
            '  <text font-size="0">񀀁</text>\n'
            '  <svg x="492" y="485"><g transform="translate(0.0,30.0) scale(0.01,-0.01)">'
            '<path class="sym-fill" fill="#ffffff" d="M200 750 l0 -550 550 0 550 0 0 550 0 550 -550 0 -550 0 0 -550z"/>'
            '<path class="sym-line" d="M1300 2250 l0 -750 -650 0 -650 0 0 -750 0 -750 750 0 750 0 0 1500 0 1500 -100 0 -100 0 0 -750z m0 -1500 l0 -550 -550 0 -550 0 0 550 0 550 550 0 550 0 0 -550z"/>'
            "</g></svg>\n</svg>",
        ),
    ],
)
def test_swu_symbol_svg(swu_sym, expected):
    svg = swu_symbol_svg(swu_sym)
    assert svg == expected


def test_swu_symbol_svg_invalid():
    svg = swu_symbol_svg("񆈥")
    assert (
        svg
        == '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    )


# -------------------------
# Symbol PNG
# -------------------------


def test_swu_symbol_png():
    png = swu_symbol_png("񀀁")
    assert png.startswith(b"\x89PNG")
    assert len(png) > 0


def test_swu_symbol_png_invalid():
    png = swu_symbol_png("񆈥")
    base64_png = base64.b64encode(png).decode("utf-8")[:45]
    assert (
        base64_png
        == "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAABmJLR0QA/wD/AP+gvaeTAAAAC0lEQVQImWNgAAIAAAUAAWJVMogAAAAASUVORK5CYII="[
            :45
        ]
    )


def test_swu_symbol_png_scale_width():
    png = swu_symbol_png("񀀁", {"width": 100})
    base64_png = base64.b64encode(png).decode("utf-8")[:45]
    assert (
        base64_png
        == "iVBORw0KGgoAAAANSUhEUgAAAGQAAAC8CAYAAACOjwsWAAADMklEQVR4nO3YsW0QOhRG4d9Smic9iTQZgIoybICXSJUlWCEbMEemuJYYgCEokzJ1uEiIBheJiMwpzif90q3cnM4jeguV5FPvpVZvZmP09PcqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpGASlYhCUikFQKgZBqRgEpWIQlIpBUCoGQakYBKViEJSKQVAqBkGpvGGQ1zykvS+9j72XWr2ZjdF77ums1ZvZGD2DnLd6MxujZ5DzVm9mY/QMct7qzWyMnkHOW72ZjdEzyHmrN7MxegY5b/VmNkbPIOet3szG6BnkvNWb2Rg9g5y3ejMbo2eQ81ZvZmP0DHLe6s1sjN6rglxfX3+9u7v7v0/9cnt7+9/T09OHPl9q9WY2Ru9VQW5ubur+/n5Gv11dXX17eHj4N7+9BvmTQWAMAmMQGIPAGATGIDAGgTEIjEFgDAJjEBiDwBgExiAwBoExCIxBYAwCYxAYg8AYBMYgMAaBMQiMQWAMAmMQGIPAGATGIDAGgTEIjEFgDAJjEBiDwBgExiAwBoExCIxBYAwCYxAYg8AYBMYgMAaBMQiMQWAMAmMQGIPAGATGIDAGgTEIjEFgDAJjEBiDwBgExiAwBoExCIxBYAwC80+DXFxcfL+8vHzoU788Pj6+f35+ftfnS63ezMbovSqI3sTqzWyMnkHOW72ZjdEzyHmrN7MxegY5b/VmNkbPIOet3szG6BnkvNWb2Rg9g5y3ejMbo2eQ81ZvZmP0DHLe6s1sjJ5Bzlu9mY3RM8h5qzezMXoVnfat97n3h59BBGIQGIPAGATGIDAGgfkBdVKb6v9o+1UAAAAASUVORK5CYII="[
            :45
        ]
    )


# -------------------------
# Sign normalization
# -------------------------


@pytest.mark.parametrize(
    "swu_sign, expected",
    [
        (
            "𝠀񀀒񀀚񋚥񋛩𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭",
            "𝠀񀀒񀀚񋚥񋛩𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭",
        ),
        (
            "𝠀񀀒񀀚񋚥񋛩𝠃𝤆𝤆񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C",
            "𝠀񀀒񀀚񋚥񋛩𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C",
        ),
    ],
)
def test_swu_sign_normalize(swu_sign, expected):
    norm = swu_sign_normalize(swu_sign)
    assert norm == expected


def test_swu_sign_normalize_invalid():
    norm = swu_sign_normalize("invalid")
    assert norm == ""


# -------------------------
# Sign SVG
# -------------------------


def test_swu_sign_svg():
    svg = swu_sign_svg("𝠃𝤍𝤕񀕁𝣾𝣷")
    assert svg.startswith("<svg")


def test_swu_sign_svg_invalid():
    svg = swu_sign_svg("invalid")
    assert (
        svg
        == '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    )


def test_swu_sign_svg_no_spatials():
    svg = swu_sign_svg("𝠃𝤆𝤆")
    assert svg.startswith("<svg")


# -------------------------
# Sign PNG
# -------------------------


def test_swu_sign_png():
    png = swu_sign_png("𝠃𝤍𝤕񀕁𝣾𝣷")
    assert len(png) > 0


def test_swu_sign_png_invalid():
    png = swu_sign_png("invalid")
    base64_png = base64.b64encode(png).decode("utf-8")[:45]
    assert (
        base64_png
        == "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAABmJLR0QA/wD/AP+gvaeTAAAAC0lEQVQImWNgAAIAAAUAAWJVMogAAAAASUVORK5CYII="[
            :45
        ]
    )


# -------------------------
# Column rendering
# -------------------------


@pytest.mark.parametrize(
    "column_data, options, expected_base64_prefix",
    [
        (
            [
                {
                    "x": 56,
                    "y": 20,
                    "minX": 481,
                    "minY": 471,
                    "width": 37,
                    "height": 58,
                    "lane": 0,
                    "padding": 0,
                    "segment": "sign",
                    "text": "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻",
                    "zoom": 1,
                },
                {
                    "x": 57,
                    "y": 118,
                    "minX": 482,
                    "minY": 468,
                    "width": 36,
                    "height": 65,
                    "lane": 0,
                    "padding": 0,
                    "segment": "sign",
                    "text": "𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦",
                    "zoom": 1,
                },
                {
                    "x": 39,
                    "y": 203,
                    "minX": 464,
                    "minY": 496,
                    "width": 72,
                    "height": 8,
                    "lane": 0,
                    "padding": 0,
                    "segment": "symbol",
                    "text": "񏌁𝣢𝤂",
                    "zoom": 1,
                },
            ],
            {"height": 250, "width": 150},
            "iVBORw0KGgoAAAANSUhEUgAAAJYAAAD6CAYAAABDN77DA",
        ),
    ],
)
def test_swu_column_png(column_data, options, expected_base64_prefix):
    png = swu_column_png(column_data, options)
    base64_png = base64.b64encode(png).decode("utf-8")[:45]
    assert base64_png == expected_base64_prefix


@pytest.mark.parametrize(
    "swu_text, options, expected_len",
    [
        (
            "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻 " "𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦 " "񏌁𝣢𝤂",
            {"height": 250, "width": 150},
            1,
        ),
    ],
)
def test_swu_columns_png(swu_text, options, expected_len):
    pngs = swu_columns_png(swu_text, options)
    assert len(pngs) == expected_len
    for png in pngs:
        assert len(png) > 0


@pytest.mark.parametrize(
    "column_data, options, expected",
    [
        (
            [
                {
                    "x": 56,
                    "y": 20,
                    "minX": 481,
                    "minY": 471,
                    "width": 37,
                    "height": 58,
                    "lane": 0,
                    "padding": 0,
                    "segment": "sign",
                    "text": "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻",
                    "zoom": 1,
                },
                {
                    "x": 57,
                    "y": 118,
                    "minX": 482,
                    "minY": 468,
                    "width": 36,
                    "height": 65,
                    "lane": 0,
                    "padding": 0,
                    "segment": "sign",
                    "text": "𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦",
                    "zoom": 1,
                },
                {
                    "x": 39,
                    "y": 203,
                    "minX": 464,
                    "minY": 496,
                    "width": 72,
                    "height": 8,
                    "lane": 0,
                    "padding": 0,
                    "segment": "symbol",
                    "text": "񏌁𝣢𝤂",
                    "zoom": 1,
                },
            ],
            {"height": 250, "width": 150},
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="150" height="250" viewBox="0 0 150 250">\n...\n</svg>',
        ),
    ],
)
def test_swu_column_svg(column_data, options, expected):
    svg = swu_column_svg(column_data, options)
    assert svg.startswith("<svg")


@pytest.mark.parametrize(
    "swu_text, options, expected_len",
    [
        (
            "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻 " "𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦 " "񏌁𝣢𝤂",
            {"height": 250, "width": 150},
            1,
        ),
    ],
)
def test_swu_columns_svg(swu_text, options, expected_len):
    svgs = swu_columns_svg(swu_text, options)
    assert len(svgs) == expected_len
    for svg in svgs:
        assert svg.startswith("<svg")
