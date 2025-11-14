"""
Data Types for Sutton SignWriting font functionality.
"""

from typing import NotRequired

from typing_extensions import TypedDict

from sutton_signwriting_core.datatypes import (
    SignSpatial,
    DetailSym,
    StyleObject,
    SegmentInfo,
    ColumnSegment,
    ColumnOptions,
)


class ScaleObject(TypedDict):
    """
    Scaling options to set the width or height of an image.
    """

    width: NotRequired[int]
    """Width for image."""
    height: NotRequired[int]
    """Height for image."""


__all__ = [
    "ScaleObject",
    "SignSpatial",
    "DetailSym",
    "StyleObject",
    "ColumnOptions",
    "SegmentInfo",
    "ColumnSegment",
]
