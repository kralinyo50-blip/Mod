#!/usr/bin/env python3
"""Datapack ve resource pack'i dagitim icin zip'ler.

Kullanim:  python3 tools/package_extras.py
Cikti:     dist/mikasrevs_phone_extras.zip
           dist/mikasrevs_phone_lang_pack.zip

Zip'lerin icinde pack.mcmeta kokte yer alir, boylece dogrudan
datapacks/ veya resourcepacks/ klasorune kopyalanabilir.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
TARGETS = {
    "datapacks/mikasrevs_phone_extras": "mikasrevs_phone_extras.zip",
    "resourcepacks/mikasrevs_phone_lang_pack": "mikasrevs_phone_lang_pack.zip",
}


def zip_dir(src: Path, out: Path) -> int:
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(src.rglob("*")):
            if file.is_file():
                zf.write(file, file.relative_to(src))
                count += 1
    return count


def main() -> None:
    DIST.mkdir(exist_ok=True)
    for folder, name in TARGETS.items():
        src = ROOT / folder
        if not src.is_dir():
            print(f"ATLANDI (klasor yok): {folder}")
            continue
        out = DIST / name
        count = zip_dir(src, out)
        print(f"{out.relative_to(ROOT)}  ({count} dosya, {out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
