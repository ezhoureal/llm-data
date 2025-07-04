from __future__ import annotations

import os
from typing import Any



def run_extract_text_from_html_bytes(html_bytes: bytes) -> str | None:
    from cs336_data import extract
    return extract.extract_text(html_bytes)


from cs336_data import identify
def run_identify_language(text: str) -> tuple[Any, float]:
    return identify.identify_language(text)

def run_mask_emails(text: str) -> tuple[str, int]:
    return identify.identify_email(text)


def run_mask_phone_numbers(text: str) -> tuple[str, int]:
    return identify.identify_phone_number(text)


def run_mask_ips(text: str) -> tuple[str, int]:
    return identify.identify_ip(text)


def run_classify_nsfw(text: str) -> tuple[Any, float]:
    raise NotImplementedError


def run_classify_toxic_speech(text: str) -> tuple[Any, float]:
    raise NotImplementedError


def run_classify_quality(text: str) -> tuple[Any, float]:
    raise NotImplementedError

def run_gopher_quality_filter(text: str) -> bool:
    from cs336_data import quality_filter
    return quality_filter.rate(text)


def run_exact_line_deduplication(
    input_files: list[os.PathLike], output_directory: os.PathLike
):
    from cs336_data.dedup import deduplicate_files
    deduplicate_files(input_files, output_directory)


def run_minhash_deduplication(
    input_files: list[os.PathLike],
    num_hashes: int,
    num_bands: int,
    ngrams: int,
    jaccard_threshold: float,
    output_directory: os.PathLike,
):
    from cs336_data.dedup import fuzzy_deduplicate
    fuzzy_deduplicate(
        input_files,
        num_hashes=num_hashes,
        num_bands=num_bands,
        ngram_length=ngrams,
        jaccard_threshold=jaccard_threshold,
        output_dir=output_directory,
    )
