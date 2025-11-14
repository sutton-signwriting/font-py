from typing import Dict, List, Optional

import base64

import cairosvg

from sutton_signwriting_core.swu import (
    swu_is_type,
    swu_colorize,
    swu_column_defaults_merge,
    swu_columns,
    swu_info,
    swu_parse_sign,
    swu_parse_symbol,
)

from sutton_signwriting_core.datatypes import (
    SignSpatial,
    ColumnSegment,
    ColumnOptions,
    StyleObject,
)

from .datatypes import (
    ScaleObject,
)

from sutton_signwriting_core.style import style_parse, style_compose

from sutton_signwriting_core.convert import coord_to_swu, swu_to_key, to_zoom

from .db import get_symbol_size, get_symbol_svg, get_symbols_info


def swu_symbol_normalize(swu_sym: str) -> str:
    """
    Normalizes a symbol with a minimum coordinate for a center of 500,500.

    Args:
        swu_sym: an SWU symbol key with optional coordinate and style string

    Returns:
        normalized symbol

    Example:
        >>> swu_symbol_normalize('񀀁-C')
        '񀀁𝣿𝣷-C'
    """
    parsed = swu_parse_symbol(swu_sym)
    if not parsed.get("symbol"):
        return ""

    size = get_symbol_size(swu_to_key(parsed["symbol"]))
    if not size:
        return ""

    width, height = size
    x = 500 - ((width + 1) // 2)
    y = 500 - ((height + 1) // 2)
    coord = coord_to_swu([x, y])
    style = parsed.get("style", "")

    return f'{parsed["symbol"]}{coord}{style}'


def swu_symbol_svg_body(swu_sym: str) -> str:
    """
    Creates the body of an SVG image from an SWU symbol key with an optional style string.

    Args:
        swu_sym: an SWU symbol key with optional style string

    Returns:
        symbol svg body

    Example:
        >>> swu_symbol_svg_body('񀀁-C')
        '  <text font-size="0">񆇡-C</text>\\n  <svg x="493" y="485">...</svg>'
    """
    parsed = swu_parse_symbol(swu_sym)
    if not parsed.get("symbol"):
        return ""

    res = get_symbol_svg(swu_to_key(parsed["symbol"]))
    if not res:
        return ""
    sym_svg, sym_width, sym_height = res

    styling = style_parse(parsed.get("style", ""))

    if coord := parsed.get("coord"):
        x1, y1 = coord
        x2 = 500 + (500 - x1)
        y2 = 500 + (500 - y1)
    else:
        x1 = 500 - ((sym_width + 1) // 2)
        y1 = 500 - ((sym_height + 1) // 2)
        x2 = 500 + (500 - x1)
        y2 = 500 + (500 - y1)

    sym_svg = f'  <svg x="{x1}" y="{y1}">{sym_svg}</svg>'

    detail = styling.get("detail")
    line: Optional[str] = None
    if styling.get("colorize"):
        line = swu_colorize(parsed["symbol"])
    elif detail:
        line = detail[0]

    if line:
        sym_svg = sym_svg.replace('class="sym-line"', f'class="sym-line" fill="{line}"')

    if detail and len(detail) > 1:
        fill = detail[1]
        sym_svg = sym_svg.replace(
            'class="sym-fill" fill="#ffffff"', f'class="sym-fill" fill="{fill}"'
        )

    background = ""
    if padding := styling.get("padding"):
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding
    if bg := styling.get("background"):
        background = f'\n  <rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" style="fill:{bg};" />'

    return f'  <text font-size="0">{swu_sym}</text>{background}\n{sym_svg}'


def swu_symbol_svg(swu_sym: str) -> str:
    """
    Creates an SVG image from an SWU symbol key with an optional style string.

    Args:
        swu_sym: an SWU symbol key with optional style string

    Returns:
        symbol svg

    Example:
        >>> swu_symbol_svg('񀀁-C')
        '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" ...>...</svg>'
    """
    parsed = swu_parse_symbol(swu_sym)
    blank = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    if not parsed.get("symbol"):
        return blank

    if not parsed.get("coord"):
        norm = swu_symbol_normalize(swu_sym)
        parsed = swu_parse_symbol(norm)
        if not parsed.get("symbol"):
            return blank

    styling = style_parse(parsed.get("style", ""))

    coord = parsed["coord"]
    x1, y1 = coord
    x2 = 500 + (500 - x1)
    y2 = 500 + (500 - y1)

    classes = f' class="{styling["classes"]}"' if styling.get("classes") else ""
    id_ = f' id="{styling["id"]}"' if styling.get("id") else ""

    if padding := styling.get("padding"):
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding

    sizing = ""
    zoom = styling.get("zoom", "1")
    if zoom != "x":
        zoom_val = float(zoom)
        width = round((x2 - x1) * zoom_val)
        height = round((y2 - y1) * zoom_val)
        sizing = f' width="{width}" height="{height}"'
    svg = f'<svg{classes}{id_} version="1.1" xmlns="http://www.w3.org/2000/svg"{sizing} viewBox="{x1} {y1} {(x2 - x1)} {(y2 - y1)}">\n'

    body = swu_symbol_svg_body(swu_sym)

    return svg + body + "\n</svg>"


def swu_symbol_png(swu_sym: str, scale: Optional[ScaleObject] = None) -> bytes:
    """
    Creates a binary PNG image from an SWU symbol key with an optional style string.

    Args:
        swu_sym: an SWU symbol key with optional style string
        scale: options for scaling to specific width or height

    Returns:
        symbol png bytes

    Example:
        >>> png = swu_symbol_png('񀀁-C')
        >>> png[:8] == b'\\x89PNG\\r\\n\x1a\\n'  # Valid PNG header
        True
    """
    svg = swu_symbol_svg(swu_sym)
    png = cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        output_width=scale.get("width") if scale else None,
        output_height=scale.get("height") if scale else None,
    )
    if not isinstance(png, bytes):
        raise ValueError("Failed to convert SVG to PNG")
    return png


def swu_symbol_png_data_url(swu_sym: str, scale: Optional[ScaleObject] = None) -> str:
    """
    Creates a data url PNG image from an SWU symbol key with an optional style string.

    Args:
        swu_sym: an SWU symbol key with optional style string
        scale: options for scaling to specific width or height

    Returns:
        symbol png data url

    Example:
        >>> swu_symbol_png_data_url('񀀁-C').startswith('data:image/png;base64,')
        True
    """
    png = swu_symbol_png(swu_sym, scale)
    return "data:image/png;base64," + base64.b64encode(png).decode("utf-8")


def swu_sign_normalize(swu_sign: str) -> str:
    """
    Normalizes an SWU sign for a center of 500,500.

    Args:
        swu_sign: an SWU sign with optional style string

    Returns:
        normalized sign

    Example:
        >>> swu_sign_normalize('𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭')
        '𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭'
    """
    parsed = swu_parse_sign(swu_sign)
    if not parsed.get("spatials"):
        return ""

    symbols = [swu_to_key(spatial["symbol"]) for spatial in parsed["spatials"]]
    symbolsizes = get_symbols_info(symbols)
    if not symbolsizes:
        return ""

    def bbox(spatials: List[SignSpatial]) -> Dict[str, int]:
        x1 = min(s["coord"][0] for s in spatials)
        y1 = min(s["coord"][1] for s in spatials)
        x2 = max(
            s["coord"][0] + symbolsizes[swu_to_key(s["symbol"])]["width"]
            for s in spatials
        )
        y2 = max(
            s["coord"][1] + symbolsizes[swu_to_key(s["symbol"])]["height"]
            for s in spatials
        )
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

    hsyms = [s for s in parsed["spatials"] if swu_is_type(s["symbol"], "hcenter")]

    vsyms = [s for s in parsed["spatials"] if swu_is_type(s["symbol"], "vcenter")]

    abox = bbox(parsed["spatials"])
    max_ = [abox["x2"], abox["y2"]]

    if hsyms:
        hbox = bbox(hsyms)
        abox["x1"] = hbox["x1"]
        abox["x2"] = hbox["x2"]

    if vsyms:
        vbox = bbox(vsyms)
        abox["y1"] = vbox["y1"]
        abox["y2"] = vbox["y2"]

    offset = [
        (abox["x2"] + abox["x1"]) // 2 - 500,
        (abox["y2"] + abox["y1"]) // 2 - 500,
    ]

    sequence_part = "𝠀" + "".join(parsed["sequence"]) if parsed.get("sequence") else ""
    box = parsed["box"]
    new_max_str = coord_to_swu([max_[0] - offset[0], max_[1] - offset[1]])
    spatials_str = "".join(
        [
            s["symbol"]
            + coord_to_swu([s["coord"][0] - offset[0], s["coord"][1] - offset[1]])
            for s in parsed["spatials"]
        ]
    )
    style = parsed.get("style", "")

    return sequence_part + box + new_max_str + spatials_str + style


def swu_sign_svg_body(swu_sign: str) -> str:
    """
    Creates the body of an SVG image from an SWU sign with an optional style string.

    Args:
        swu_sign: an SWU sign with optional style string

    Returns:
        sign svg body

    Example:
        >>> swu_sign_svg_body('𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C')
        '  <text font-size="0">𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C</text>\\n  <svg x="476" y="466">...</svg>...'
    """
    parsed = swu_parse_sign(swu_sign)
    spatials = parsed.get("spatials")
    if not spatials:
        return (
            ""  # Or call swu_symbol_svg_body if desired, but matching JS returns blank
        )

    styling = style_parse(parsed.get("style", ""))

    # Apply detailsym to spatials
    if detailsym := styling.get("detailsym"):
        for sym in detailsym:
            index = sym.get("index", 0) - 1
            if 0 <= index < len(spatials):
                spatials[index]["detail"] = sym.get("detail", [])

    syms_info = get_symbols_info([swu_to_key(s["symbol"]) for s in spatials])

    x_coords = [s["coord"][0] for s in spatials]
    y_coords = [s["coord"][1] for s in spatials]
    x1 = min(x_coords)
    y1 = min(y_coords)
    x2, y2 = parsed["max"]

    background = ""
    if padding := styling.get("padding"):
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding
    if bg := styling.get("background"):
        background = f'\n  <rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" style="fill:{bg};" />'

    svg_body = f'  <text font-size="0">{swu_sign}</text>{background}'

    detail = styling.get("detail", [])

    line_base = detail[0] if detail else ""
    fill_base = detail[1] if len(detail) > 1 else ""

    svgs: List[str] = []
    for spatial in spatials:
        symbol = spatial["symbol"]
        coord = spatial["coord"]
        info = syms_info.get(swu_to_key(symbol))
        if not info:
            continue
        sym_svg = info["svg"]

        # Line color
        line = line_base
        if "detail" in spatial and spatial["detail"]:
            line = spatial["detail"][0]
        elif styling.get("colorize"):
            line = swu_colorize(symbol)
        if line:
            sym_svg = sym_svg.replace(
                'class="sym-line"', f'class="sym-line" fill="{line}"'
            )

        # Fill color
        fill = fill_base
        if "detail" in spatial and len(spatial["detail"]) > 1:
            fill = spatial["detail"][1]
        if fill:
            sym_svg = sym_svg.replace(
                'class="sym-fill" fill="#ffffff"', f'class="sym-fill" fill="{fill}"'
            )

        svgs.append(f'  <svg x="{coord[0]}" y="{coord[1]}">{sym_svg}</svg>')

    if svgs:
        svg_body += "\n" + "\n".join(svgs)

    return svg_body


def swu_sign_svg(swu_sign: str) -> str:
    """
    Creates an SVG image from an SWU sign with an optional style string.

    Args:
        swu_sign: an SWU sign with optional style string

    Returns:
        sign svg

    Example:
        >>> swu_sign_svg('𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C')
        '<svg ...> ... </svg>'
    """
    parsed = swu_parse_sign(swu_sign)
    blank = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    if not parsed.get("box"):
        return blank

    info = swu_info(swu_sign)
    x1 = info["minX"]
    y1 = info["minY"]
    x2 = x1 + info["width"]
    y2 = y1 + info["height"]

    styling = style_parse(parsed.get("style", ""))

    classes = f' class="{styling["classes"]}"' if styling.get("classes") else ""
    id_ = f' id="{styling["id"]}"' if styling.get("id") else ""

    padding = styling.get("padding", 0) + info["padding"]
    x1 -= padding
    y1 -= padding
    x2 += padding
    y2 += padding

    sizing = ""
    zoom = to_zoom(styling.get("zoom")) * to_zoom(info["zoom"])
    if zoom != "x":
        sizing = f' width="{(x2 - x1) * zoom}" height="{(y2 - y1) * zoom}"'

    svg = f'<svg{classes}{id_} version="1.1" xmlns="http://www.w3.org/2000/svg"{sizing} viewBox="{x1} {y1} {(x2 - x1)} {(y2 - y1)}" preserveAspectRatio="xMidYMid meet">\n'

    body = swu_sign_svg_body(swu_sign)

    return svg + body + "\n</svg>"


def swu_sign_png(swu_sign: str, scale: Optional[ScaleObject] = None) -> bytes:
    """
    Creates a binary PNG image from an SWU sign with an optional style string.

    Args:
        swu_sign: an SWU sign with optional style string
        scale: options for scaling to specific width or height

    Returns:
        sign png bytes

    Example:
        >>> png = swu_sign_png('𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C')
        >>> png[:8] == b'\\x89PNG\\r\\n\x1a\\n'  # Valid PNG header
        True
    """
    svg = swu_sign_svg(swu_sign)
    png = cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        output_width=scale.get("width") if scale else None,
        output_height=scale.get("height") if scale else None,
    )
    if not isinstance(png, bytes):
        raise ValueError("Failed to convert SVG to PNG")
    return png


def swu_sign_png_data_url(swu_sign: str, scale: Optional[ScaleObject] = None) -> str:
    """
    Creates a data url PNG image from an SWU sign with an optional style string.

    Args:
        swu_sign: an SWU sign with optional style string
        scale: options for scaling to specific width or height

    Returns:
        sign png data url

    Example:
        >>> swu_sign_png_data_url('𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭-C').startswith('data:image/png;base64,')
        True
    """
    png = swu_sign_png(swu_sign, scale)
    return "data:image/png;base64," + base64.b64encode(png).decode("utf-8")


def swu_column_svg(
    column: List[ColumnSegment], options: Optional[ColumnOptions] = None
) -> str:
    """
    Creates an SVG column image for an array of column data.

    .. note:: This is an internal helper; `column` and `options` must be generated in tandem
              by the calling function (`swu_columns_svg`) to ensure compatibility.
              Standalone use may produce incorrect output if values are mismatched.

    Args:
        column: an array of column data
        options: an object of column options

    Returns:
        svg column

    Example:
        >>> col = [{"x": 56, "y": 20, "minX": 481, "minY": 471, "width": 37, "height": 58, "lane": 0, "padding": 0, "segment": "sign", "text": "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻", "zoom": 1}]
        >>> swu_column_svg(col, {"height": 250, "width": 150}).startswith('<svg')
        True
    """
    blank = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'
    if not isinstance(column, list):
        return blank

    values = swu_column_defaults_merge(options)
    x1 = 0
    y1 = 0
    x2 = values["width"]
    y2 = values["height"]

    background = ""
    if values.get("background"):
        background = f'  <rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" style="fill:{values["background"]};" />\n'

    sizing = f' width="{values["width"]}" height="{values["height"]}"'

    svg = f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg"{sizing} viewBox="{x1} {y1} {(x2 - x1)} {(y2 - y1)}">\n{background}'

    for item in column:
        dash_index = item["text"].find("-")
        if dash_index > 0:
            item_style = item["text"][dash_index:]
            new_style: StyleObject = {**values["style"], **style_parse(item_style)}
            item["text"] = item["text"].replace(
                item_style, style_compose(new_style) or ""
            )
        else:
            item["text"] += style_compose(values["style"]) or ""

        item["zoom"] = to_zoom(item["zoom"]) * to_zoom(values["style"]["zoom"])

        svg += f'<g transform="translate({item["x"]},{item["y"]}) scale({item["zoom"]}) translate({-item["minX"]},{-item["minY"]}) ">\n'
        if item["segment"] == "sign":
            svg += swu_sign_svg_body(item["text"])
        else:
            svg += swu_symbol_svg_body(item["text"])
        svg += "\n</g>\n"

    svg += "</svg>"

    return svg


def swu_column_png(
    column: List[ColumnSegment], options: Optional[ColumnOptions] = None
) -> bytes:
    """
    Creates a binary PNG column image for an array of column data.

    .. note:: This is an internal helper; `column` and `options` must be generated in tandem
              by the calling function (`swu_columns_png`) to ensure compatibility.
              Standalone use may produce incorrect output if values are mismatched.

    Args:
        column: an array of column data
        options: an object of column options

    Returns:
        png column bytes

    Example:
        >>> col = [{"x": 56, "y": 20, "minX": 481, "minY": 471, "width": 37, "height": 58, "lane": 0, "padding": 0, "segment": "sign", "text": "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻", "zoom": 1}]
        >>> len(swu_column_png(col, {"height": 250, "width": 150})) > 0
        True
    """
    svg = swu_column_svg(column, options)
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    if not isinstance(png, bytes):
        raise ValueError("Failed to convert SVG to PNG")
    return png


def swu_columns_svg(
    swu_text: str, options: Optional[ColumnOptions] = None
) -> List[str]:
    """
    Creates an array of SVG column images for an SWU text.

    Args:
        swu_text: a text of SWU signs and punctuation
        options: an object of column options

    Returns:
        array of svg columns

    Example:
        >>> swu_text = "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻 𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦 񏌁𝣢𝤂"
        >>> opts = {"height": 250, "width": 150}
        >>> len(swu_columns_svg(swu_text, opts))
        1
    """
    cols = swu_columns(swu_text, options)
    svgs = []
    for i, col in enumerate(cols["columns"]):
        svgs.append(
            swu_column_svg(col, {**cols["options"], "width": cols["widths"][i]})
        )
    return svgs


def swu_columns_png(
    swu_text: str, options: Optional[ColumnOptions] = None
) -> List[bytes]:
    """
    Creates an array of PNG column images for an SWU text.

    Args:
        swu_text: a text of SWU signs and punctuation
        options: an object of column options

    Returns:
        array of PNG data

    Example:
        >>> swu_text = "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻 𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦 񏌁𝣢𝤂"
        >>> opts = {"height": 250, "width": 150}
        >>> len(swu_columns_png(swu_text, opts))
        1
    """
    svgs = swu_columns_svg(swu_text, options)
    pngs = []
    for svg in svgs:
        png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
        pngs.append(png)
    return pngs


def swu_columns_png_data_url(
    swu_text: str, options: Optional[ColumnOptions] = None
) -> List[str]:
    """
    Creates an array of PNG data url column images for an SWU text.

    Args:
        swu_text: a text of SWU signs and punctuation
        options: an object of column options

    Returns:
        array of PNG data urls

    Example:
        >>> swu_text = "𝠀񁲡񈩧𝠃𝤘𝤣񁲡𝣳𝣩񈩧𝤉𝣻 𝠀񃊢񃊫񋛕񆇡𝠃𝤘𝤧񃊫𝣻𝤕񃊢𝣴𝣼񆇡𝤎𝤂񋛕𝤆𝣦 񏌁𝣢𝤂"
        >>> opts = {"height": 250, "width": 150}
        >>> all(u.startswith('data:image/png;base64,') for u in swu_columns_png_data_url(swu_text, opts))
        True
    """
    pngs = swu_columns_png(swu_text, options)
    return [
        "data:image/png;base64," + base64.b64encode(png).decode("utf-8") for png in pngs
    ]


__all__ = [
    "swu_symbol_normalize",
    "swu_symbol_svg_body",
    "swu_symbol_svg",
    "swu_symbol_png",
    "swu_symbol_png_data_url",
    "swu_sign_normalize",
    "swu_sign_svg_body",
    "swu_sign_svg",
    "swu_sign_png",
    "swu_sign_png_data_url",
    "swu_column_svg",
    "swu_column_png",
    "swu_columns_svg",
    "swu_columns_png",
    "swu_columns_png_data_url",
]
