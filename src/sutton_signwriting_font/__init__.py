"""
sutton_signwriting_font – public entry point.
"""

from __future__ import annotations

from .db import (
    get_db_path,
    get_symbol_size,
    get_symbol_svg,
    get_symbols_info,
)

from .fsw import (
    fsw_symbol_normalize,
    fsw_symbol_svg_body,
    fsw_symbol_svg,
    fsw_symbol_png,
    fsw_symbol_png_data_url,
    fsw_sign_normalize,
    fsw_sign_svg_body,
    fsw_sign_svg,
    fsw_sign_png,
    fsw_sign_png_data_url,
    fsw_column_svg,
    fsw_column_png,
    fsw_columns_svg,
    fsw_columns_png,
    fsw_columns_png_data_url,
)

from .swu import (
    swu_symbol_normalize,
    swu_symbol_svg_body,
    swu_symbol_svg,
    swu_symbol_png,
    swu_symbol_png_data_url,
    swu_sign_normalize,
    swu_sign_svg_body,
    swu_sign_svg,
    swu_sign_png,
    swu_sign_png_data_url,
    swu_column_svg,
    swu_column_png,
    swu_columns_svg,
    swu_columns_png,
    swu_columns_png_data_url,
)

from .datatypes import (
    ScaleObject,
    SignSpatial,
    ColumnSegment,
    ColumnOptions,
    StyleObject,
)


__all__ = [
    # DB
    "get_db_path",
    "get_symbol_size",
    "get_symbol_svg",
    "get_symbols_info",
    # FSW
    "fsw_symbol_normalize",
    "fsw_symbol_svg_body",
    "fsw_symbol_svg",
    "fsw_symbol_png",
    "fsw_symbol_png_data_url",
    "fsw_sign_normalize",
    "fsw_sign_svg_body",
    "fsw_sign_svg",
    "fsw_sign_png",
    "fsw_sign_png_data_url",
    "fsw_column_svg",
    "fsw_column_png",
    "fsw_columns_svg",
    "fsw_columns_png",
    "fsw_columns_png_data_url",
    # SWU
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
    # Data types
    "ScaleObject",
    "SignSpatial",
    "ColumnSegment",
    "ColumnOptions",
    "StyleObject",
]

__version__ = "1.0.0"
