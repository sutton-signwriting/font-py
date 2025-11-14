import base64

import pytest

from sutton_signwriting_font.fsw import (
    fsw_column_png,
    fsw_column_svg,
    fsw_columns_png,
    fsw_columns_svg,
    fsw_sign_normalize,
    fsw_sign_png,
    fsw_sign_svg,
    fsw_symbol_normalize,
    fsw_symbol_png,
    fsw_symbol_svg,
)

# -------------------------
# Symbol normalization
# -------------------------


@pytest.mark.parametrize(
    "fsw_sym, expected",
    [
        ("S20500", "S20500495x494"),
        ("S20500500x500", "S20500495x494"),
        ("S20500500x500-C", "S20500495x494-C"),
    ],
)
def test_fsw_symbol_normalize(fsw_sym, expected):
    norm = fsw_symbol_normalize(fsw_sym)
    assert norm == expected


def test_fsw_symbol_normalize_invalid():
    norm = fsw_symbol_normalize("S2055f")
    assert norm == ""


# -------------------------
# Symbol SVG
# -------------------------


@pytest.mark.parametrize(
    "fsw_sym, expected",
    [
        (
            "S10000",
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="16" height="30" viewBox="492 485 16 30">\n'
            '  <text font-size="0">S10000</text>\n'
            '  <svg x="492" y="485"><g transform="translate(0.0,30.0) scale(0.01,-0.01)">'
            '<path class="sym-fill" fill="#ffffff" d="M200 750 l0 -550 550 0 550 0 0 550 0 550 -550 0 -550 0 0 -550z"/>'
            '<path class="sym-line" d="M1300 2250 l0 -750 -650 0 -650 0 0 -750 0 -750 750 0 750 0 0 1500 0 1500 -100 0 -100 0 0 -750z m0 -1500 l0 -550 -550 0 -550 0 0 550 0 550 550 0 550 0 0 -550z"/>'
            "</g></svg>\n</svg>",
        ),
    ],
)
def test_fsw_symbol_svg(fsw_sym, expected):
    svg = fsw_symbol_svg(fsw_sym)
    assert svg == expected


def test_fsw_symbol_svg_invalid():
    svg = fsw_symbol_svg("S20544")
    assert (
        svg
        == '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    )


# -------------------------
# Symbol PNG
# -------------------------


def test_fsw_symbol_png():
    png = fsw_symbol_png("S10000")
    assert png.startswith(b"\x89PNG")
    assert len(png) > 0


def test_fsw_symbol_png_invalid():
    png = fsw_symbol_png("S20544")
    base64_png = base64.b64encode(png).decode("utf-8")[:45]
    assert (
        base64_png
        == "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAABmJLR0QA/wD/AP+gvaeTAAAAC0lEQVQImWNgAAIAAAUAAWJVMogAAAAASUVORK5CYII="[
            :45
        ]
    )


def test_fsw_symbol_png_scale_width():
    png = fsw_symbol_png("S10000", {"width": 100})
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
    "fsw_sign, expected",
    [
        (
            "AS10011S10019S2e704S2e748M525x535S2e748483x510S10011501x466S2e704510x500S10019476x475",
            "AS10011S10019S2e704S2e748M525x535S2e748483x510S10011501x466S2e704510x500S10019476x475",
        ),
        (
            "AS10011S10019S2e704S2e748M500x500S2e748483x510S10011501x466S2e704510x500S10019476x475-C",
            "AS10011S10019S2e704S2e748M525x535S2e748483x510S10011501x466S2e704510x500S10019476x475-C",
        ),
    ],
)
def test_fsw_sign_normalize(fsw_sign, expected):
    norm = fsw_sign_normalize(fsw_sign)
    assert norm == expected


def test_fsw_sign_normalize_invalid():
    norm = fsw_sign_normalize("invalid")
    assert norm == ""


# -------------------------
# Sign SVG
# -------------------------


def test_fsw_sign_svg():
    svg = fsw_sign_svg("M507x515S10e00492x485")
    assert svg.startswith("<svg")


def test_fsw_sign_svg_invalid():
    svg = fsw_sign_svg("invalid")
    assert (
        svg
        == '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    )


def test_fsw_sign_svg_no_spatials():
    svg = fsw_sign_svg("M500x500")
    assert svg.startswith("<svg")


# -------------------------
# Sign PNG
# -------------------------


def test_fsw_sign_png():
    png = fsw_sign_png("M507x515S10e00492x485")
    assert len(png) > 0


def test_fsw_sign_png_invalid():
    png = fsw_sign_png("invalid")
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
                    "text": "AS14c20S27106M518x529S14c20481x471S27106503x489",
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
                    "text": "AS18701S1870aS2e734S20500M518x533S1870a489x515S18701482x490S20500508x496S2e734500x468",
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
                    "text": "S38800464x496",
                    "zoom": 1,
                },
            ],
            {"height": 250, "width": 150},
            "iVBORw0KGgoAAAANSUhEUgAAAJYAAAD6CAYAAABDN77DA",
        ),
    ],
)
def test_fsw_column_png(column_data, options, expected_base64_prefix):
    png = fsw_column_png(column_data, options)
    base64_png = base64.b64encode(png).decode("utf-8")[:45]
    assert base64_png == expected_base64_prefix


@pytest.mark.parametrize(
    "fsw_text, options, expected_len",
    [
        (
            "AS14c20S27106M518x529S14c20481x471S27106503x489 "
            "AS18701S1870aS2e734S20500M518x533S1870a489x515S18701482x490S20500508x496S2e734500x468 "
            "S38800464x496",
            {"height": 250, "width": 150},
            1,
        ),
    ],
)
def test_fsw_columns_png(fsw_text, options, expected_len):
    pngs = fsw_columns_png(fsw_text, options)
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
                    "text": "AS14c20S27106M518x529S14c20481x471S27106503x489",
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
                    "text": "AS18701S1870aS2e734S20500M518x533S1870a489x515S18701482x490S20500508x496S2e734500x468",
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
                    "text": "S38800464x496",
                    "zoom": 1,
                },
            ],
            {"height": 250, "width": 150},
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="150" height="250" viewBox="0 0 150 250">\n...\n</svg>',
        ),
    ],
)
def test_fsw_column_svg(column_data, options, expected):
    svg = fsw_column_svg(column_data, options)
    assert svg.startswith("<svg")


@pytest.mark.parametrize(
    "fsw_text, options, expected_len",
    [
        (
            "AS14c20S27106M518x529S14c20481x471S27106503x489 "
            "AS18701S1870aS2e734S20500M518x533S1870a489x515S18701482x490S20500508x496S2e734500x468 "
            "S38800464x496",
            {"height": 250, "width": 150},
            1,
        ),
    ],
)
def test_fsw_columns_svg(fsw_text, options, expected_len):
    svgs = fsw_columns_svg(fsw_text, options)
    assert len(svgs) == expected_len
    for svg in svgs:
        assert svg.startswith("<svg")
