import sqlite3
from importlib.resources import files
from typing import Dict, List, Optional, Tuple, TypedDict


class SymbolInfo(TypedDict):
    svg: str
    width: int
    height: int


def get_db_path() -> str:
    """Returns the path to the bundled SQLite database."""
    return str(files("sutton_signwriting_font").joinpath("db", "iswa2010.db"))


def get_symbol_size(key: str) -> Optional[Tuple[int, int]]:
    """
    Queries the width and height for a symbol key.

    Args:
        key: FSW symbol key (e.g., 'S10000')

    Returns:
        Tuple of (width, height) if found, else None.
    """
    conn = sqlite3.connect(get_db_path())
    try:
        cur = conn.cursor()
        res = cur.execute(
            "SELECT width, height FROM symbol WHERE symkey = ?", (key,)
        ).fetchone()
        return res if res else None
    finally:
        conn.close()


def get_symbol_svg(key: str) -> Optional[Tuple[str, int, int]]:
    """
    Queries the SVG fragment, width, and height for a symbol key.

    Args:
        key: FSW symbol key

    Returns:
        Tuple of (svg_fragment, width, height) if found, else None.
    """
    conn = sqlite3.connect(get_db_path())
    try:
        cur = conn.cursor()
        res = cur.execute(
            "SELECT svg, width, height FROM symbol WHERE symkey = ?", (key,)
        ).fetchone()
        return res if res else None
    finally:
        conn.close()


def get_symbols_info(keys: List[str]) -> Dict[str, SymbolInfo]:
    """
    Batch queries SVG fragments, widths, and heights for multiple symbol keys.

    Args:
        keys: List of FSW symbol keys

    Returns:
        Dict mapping key to {'svg': str, 'width': int, 'height': int}
    """
    if not keys:
        return {}
    conn = sqlite3.connect(get_db_path())
    try:
        cur = conn.cursor()
        placeholders = ",".join("?" for _ in keys)
        res = cur.execute(
            f"SELECT symkey, svg, width, height FROM symbol WHERE symkey IN ({placeholders})",
            keys,
        ).fetchall()
        return {
            row[0]: {"svg": row[1], "width": row[2], "height": row[3]} for row in res
        }
    finally:
        conn.close()


__all__ = [
    "get_db_path",
    "get_symbol_size",
    "get_symbol_svg",
    "get_symbols_info",
]
