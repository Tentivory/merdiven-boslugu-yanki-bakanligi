#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merdiven Boşluğu Yankı Bakanlığı — çalışan resmi simülatör.

Bağırırsın. Beton düşünür. Komşu duyduğunu sanır. Tutanak çıkar.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
import time
import unicodedata

KOMŞULAR = [
    "3. kat Feride Hanım (terlik istihbaratı)",
    "1. kat kapıcı Rıza (paspas anayasası)",
    "5. kat sessizlik derneği başkanı",
    "bodrumdaki kedi (oy hakkı yok, veto hakkı var)",
    "4. kat çöp saati komiseri",
]

SIKAYETLER = [
    "duyduğu cümleyi market ilanı sandı",
    "yankıyı kişisel hakaret olarak tutanağa geçirdi",
    "sesin yönünü şaşırıp kendi kapısını çaldı",
    "genelgedeki sessizlik maddesini ezbere okudu, madde yoktu",
    "yankıyı kayıt altına alıp ertesi gün çayına kattı",
]


def kat_gecikmesi(kat: int) -> float:
    return max(1, kat) * 0.12


def yanki_uret(metin: str, kat: int) -> list[str]:
    parcalar = []
    kalan = metin.strip()
    for i in range(max(1, kat)):
        if not kalan:
            kalan = "ı"
        kes = max(1, len(kalan) - 1 - (i % 3))
        parca = kalan[:kes]
        if i % 2 == 1:
            parca = parca.lower()
        if i == kat - 1:
            unluler = [c for c in parca if c.lower() in "aeıioöuü"]
            parca = "".join(unluler) or "a"
        parcalar.append(parca)
        kalan = parca
    return parcalar


def dosya_no(metin: str) -> str:
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:8].upper()
    return f"MBYB-2026-{ozet}"


def tutanak(metin: str, kat: int, bekle: bool) -> str:
    if bekle:
        time.sleep(min(kat_gecikmesi(kat), 1.5))
    yankilar = yanki_uret(metin, kat)
    komsu = random.choice(KOMŞULAR)
    sikayet = random.choice(SIKAYETLER)
    karar = "YANKI KABUL" if len(metin) % 2 == 0 else "YANKI İADE"
    satirlar = [
        "=" * 54,
        "MERDİVEN BOŞLUĞU YANKI BAKANLIĞI",
        f"Dosya: {dosya_no(metin)}   Kat: {kat}",
        "=" * 54,
        f"Asıl cümle : {metin}",
        "Yankı zinciri:",
    ]
    for i, y in enumerate(yankilar, start=1):
        girinti = " " * i
        satirlar.append(f"  {girinti}{i}. kat -> {y}")
    satirlar += [
        f"Komşu      : {komsu}",
        f"Şikayet    : {sikayet}",
        f"Karar      : {karar}",
        "Gerekçe    : Beton duydu, evrak yazdı, anlam aranmadı.",
        "-" * 54,
        "DAMGA: Kayyum Grok | Tentivory | 7 Ekim 2026",
        "Mühür ciddidir. Mühürü basan kişi de ciddidir. İş ciddi değildir.",
        "=" * 54,
    ]
    return "\n".join(satirlar)


def demo() -> str:
    ornekler = [
        ("anahtarım düştü", 4),
        ("çay demlendi inen var mı", 3),
        ("sessizlik lütfen", 6),
    ]
    return "\n\n".join(tutanak(m, k, bekle=False) for m, k in ornekler)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Merdiven boşluğu yankı tutanağı üretir.")
    p.add_argument("cumle", nargs="*", help="Boşluğa bağırılacak cümle")
    p.add_argument("--kat", type=int, default=4, help="Kat sayısı (1-12)")
    p.add_argument("--demo", action="store_true", help="Üç örnek dosya bas")
    p.add_argument("--hizli", action="store_true", help="Beton gecikmesini atla")
    args = p.parse_args(argv)
    if args.demo:
        print(demo())
        return 0
    metin = " ".join(args.cumle).strip()
    if not metin:
        p.print_help()
        return 1
    kat = min(12, max(1, args.kat))
    # normalize, çünkü beton unicode sevmez ama tahammül eder
    metin = unicodedata.normalize("NFC", metin)
    print(tutanak(metin, kat, bekle=not args.hizli))
    return 0


if __name__ == "__main__":
    sys.exit(main())
