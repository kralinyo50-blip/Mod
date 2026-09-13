#!/usr/bin/env python3
"""Depodaki datapack / resource pack dosyalarini dogrular.

Kullanim:  python3 tools/validate.py
CI'da her push'ta calisir (.github/workflows/validate.yml).
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAR = ROOT / "mikasrevs_phone-1.3.3.jar"
PACKS = ["datapacks/mikasrevs_phone_extras", "resourcepacks/mikasrevs_phone_lang_pack"]

errors: list[str] = []
warnings: list[str] = []


def load_json(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Gecersiz JSON: {path.relative_to(ROOT)} -> {exc}")
        return None


def normalize(key: str) -> str:
    """iki namespace'i esit say: mattupolis_phone (eski) == mikasrevs_phone (aktif)."""
    return key.replace("mattupolis_phone", "mikasrevs_phone")


def reference_keys() -> set[str]:
    """JAR icindeki tum en_us.json anahtarlarini referans al (varsa)."""
    if not JAR.exists():
        warnings.append("JAR bulunamadi, dil anahtari karsilastirmasi atlandi.")
        return set()
    keys: set[str] = set()
    with zipfile.ZipFile(JAR) as zf:
        for name in (n for n in zf.namelist() if n.endswith("lang/en_us.json")):
            with zf.open(name) as fh:
                keys.update(normalize(k) for k in json.load(fh))
    return keys


def main() -> int:
    ref = reference_keys()

    for pack in PACKS:
        pack_dir = ROOT / pack
        if not pack_dir.is_dir():
            errors.append(f"Paket klasoru yok: {pack}")
            continue

        mcmeta = pack_dir / "pack.mcmeta"
        if not mcmeta.exists():
            errors.append(f"{pack}: pack.mcmeta eksik")
        else:
            data = load_json(mcmeta)
            if data is not None and "pack" not in data:
                errors.append(f"{pack}: pack.mcmeta icinde 'pack' alani yok")
            if data is not None and data.get("pack", {}).get("pack_format") != 15:
                warnings.append(f"{pack}: pack_format 15 degil (1.20.1 icin 15 olmali)")

        for json_file in sorted(pack_dir.rglob("*.json")):
            data = load_json(json_file)
            if data is None:
                continue

            rel = json_file.relative_to(pack_dir)
            # dil dosyalari: anahtar eslesmesi
            if rel.parent.match("lang") and ref:
                current = {normalize(k) for k in data}
                missing = sorted(ref - current)
                extra = sorted(current - ref)
                if missing:
                    warnings.append(f"{pack}/{rel}: eksik anahtar -> {missing}")
                if extra:
                    warnings.append(f"{pack}/{rel}: fazla anahtar -> {extra}")

            # tarif dosyalari: zorunlu alanlar
            if rel.parent.name == "recipes":
                for field in ("type", "result"):
                    if field not in data:
                        errors.append(f"{pack}/{rel}: '{field}' alani eksik")
                if "ingredients" not in data and "pattern" not in data:
                    errors.append(f"{pack}/{rel}: ingredients veya pattern alani eksik")

            # basarim dosyalari
            if rel.parent.name == "advancements":
                for field in ("criteria",):
                    if field not in data:
                        errors.append(f"{pack}/{rel}: '{field}' alani eksik")

    print(f"Kontrol edilen paket: {len(PACKS)}")
    for w in warnings:
        print(f"UYARI  {w}")
    for e in errors:
        print(f"HATA   {e}")
    if errors:
        print(f"\n{len(errors)} hata, {len(warnings)} uyari -> BASARISIZ")
        return 1
    print(f"\n{len(warnings)} uyari -> TAMAM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
