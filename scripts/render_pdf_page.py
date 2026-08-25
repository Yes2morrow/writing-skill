#!/usr/bin/env python3
"""Render one PDF page for visual extraction-quality checks."""

from __future__ import annotations

import argparse
from pathlib import Path

import pypdfium2 as pdfium


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--page", type=int, default=1, help="One-based page number")
    parser.add_argument("--scale", type=float, default=1.6)
    args = parser.parse_args()

    document = pdfium.PdfDocument(str(args.pdf))
    try:
        if not 1 <= args.page <= len(document):
            raise SystemExit(f"page must be between 1 and {len(document)}")
        page = document[args.page - 1]
        try:
            image = page.render(scale=args.scale).to_pil()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            image.save(args.output)
        finally:
            page.close()
    finally:
        document.close()


if __name__ == "__main__":
    main()
