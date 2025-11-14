# sutton-signwriting-font
[![Source Code on GitHub](https://img.shields.io/badge/source-GitHub-lightgrey?logo=github)](https://github.com/sutton-signwriting/font-py)
[![Docs](https://img.shields.io/badge/docs-sutton--signwriting.io-blue)](https://www.sutton-signwriting.io/font-py)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/sutton-signwriting/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Spec](https://img.shields.io/badge/spec-Formal%20SignWriting-blueviolet)](https://datatracker.ietf.org/doc/html/draft-slevinski-formal-signwriting)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17553763.svg)](https://doi.org/10.5281/zenodo.17553763)


[![PyPI](https://img.shields.io/pypi/v/sutton-signwriting-font)](https://pypi.org/project/sutton-signwriting-font/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sutton-signwriting-font)](https://pypistats.org/packages/sutton-signwriting-font)
[![CI](https://github.com/sutton-signwriting/font-py/actions/workflows/ci.yml/badge.svg)](https://github.com/sutton-signwriting/font-py/actions)


`sutton-signwriting-font` is a Python library that generates SVG and PNG images for individual symbols, complete signs, and structured text.
The library covers the entire set of the International SignWritnig Alphabet 2010 (ISWA 2010).

This library builds on `sutton-signwriting-core` for parsing Formal SignWriting in ASCII (FSW) and SignWriting in Unicode (SWU), and uses an SQLite database of SVG fragments to compose self-contained visualizations. See [draft-slevinski-formal-signwriting](https://www.ietf.org/archive/id/draft-slevinski-formal-signwriting-10.html) for detailed specification.

> **Author:** [Steve Slevinski](https://steveslevinski.me)  
**Channel:** [YouTube](https://www.youtube.com/channel/UCXu4AXlG0rXFtk_5SzumDow)  
**Support:** [Patreon](https://www.patreon.com/signwriting)  
**Donate:** [sutton-signwriting.io](https://donate.sutton-signwriting.io)

## Useful Links

- **Source:** [GitHub](https://github.com/sutton-signwriting/font-py)
- **PyPI:** [pypi.org/project/sutton-signwriting-font](https://pypi.org/project/sutton-signwriting-font/)
- **Documentation:** [sutton-signwriting.io/font-py](https://www.sutton-signwriting.io/font-py)
- **Issues:** [GitHub Issues](https://github.com/sutton-signwriting/font-py/issues)
- **Discussion:** [Gitter](https://gitter.im/sutton-signwriting/community)

---

## Installation

```bash
pip install sutton-signwriting-font
```

---

## Usage

```python
from sutton_signwriting_core.render import (
    fsw_symbol_svg, fsw_sign_svg,
    fsw_columns_svg, fsw_symbol_png
)

# Symbol SVG
svg = fsw_symbol_svg('S20500-C')
# Returns SVG string

# Sign SVG
svg = fsw_sign_svg('M525x535S2e748483x510S10011501x466S2e704510x500S10019476x475')
# Returns SVG string

# Text SVG
svg_list = fsw_columns_svg(
    'AS14c20S27106M518x529S14c20481x471S27106503x489 AS18701S1870aS2e734S20500M518x533S1870a489x515S18701482x490S20500508x496S2e734500x468 S38800464x496',
    {'height': 250, 'width': 150, 'pad': 20}
)
# Returns list of SVG strings (one per column)

# Symbol PNG
png_bytes: bytes = fsw_symbol_png('S20500', {'width': 256})
# Returns PNG bytes
```

All functions are **fully typed**, **validated**, and **documented** with Python-style docstrings (Google format). Run `help(fsw_symbol_svg)` for details.

---

## Development

```bash
# 1. Clone the repo
git clone https://github.com/sutton-signwriting/font-py.git
cd font-py

# 2. Install Poetry (if you don’t have it)
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

# 3. Create the virtual environment and install deps
poetry install

# 4. Activate the environment (Poetry 2+)
poetry env activate
#   (copy and execute the returned command)

# 5. Run the test suite
pytest -v

# 6. Code coverage and HTML report
pytest --cov
pytest -v --cov=sutton_signwriting_font --cov-report=html
pytest --cov=sutton_signwriting_font --cov-report=xml

# 7. Lint / format / type-check
black .
ruff check .
mypy src

# 8. Update Version string
pyproject.toml:version = "1.0.0"
src/sutton_signwriting_font/__init__.py:__version__ = "1.0.0"
sphinx-docs/source/conf.py:release = "1.0.0"
sphinx-docs/source/conf.py:version = "1.0"

# 9. Create HTML documentation
cd sphinx-docs
sphinx-build -b html -a -E source/ ../docs/

# 10. Build distributions
poetry build

# 11. Publish to pypi
poetry publish

# 12. Git commit, push, and tag
git commit -m "message"
git push origin main
git tag v1.0.0 && git push --tags
```

---

## License

MIT – see [`LICENSE`](LICENSE) for details.
> *Maintained by Steve Slevinski – <Slevinski@signwriting.org>*

---

## SignWriting Resources

- **Website:** [signwriting.org](https://signwriting.org/)
- **Resources:** [sutton-signwriting.io](https://www.sutton-signwriting.io/)
- **Wikipedia:** [SignWriting](https://en.wikipedia.org/wiki/SignWriting)
- **Grokipedia** [SignWriting](https://grokipedia.com/page/SignWriting)
- **Forum:** [swlist](https://www.signwriting.org/forums/swlist/)
- **Facebook:** [Sutton SignWriting Group](https://www.facebook.com/groups/SuttonSignWriting/)
