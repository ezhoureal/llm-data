import os

def deduplicate_files(input_paths, output_dir):
    # Collect all lines from all input files
    line_counts = {}
    for path in input_paths:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line_counts[line] = line_counts.get(line, 0) + 1

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write deduplicated files
    for path in input_paths:
        basename = os.path.basename(path)
        output_path = os.path.join(output_dir, basename)
        with open(path, 'r', encoding='utf-8') as fin, \
             open(output_path, 'w', encoding='utf-8') as fout:
            for line in fin:
                if line_counts[line] == 1:
                    fout.write(line)

import os
import re
import unicodedata
import random
import hashlib
from collections import defaultdict

def normalize_text(text):
    # Apply NFD Unicode normalization
    text = unicodedata.normalize('NFD', text)
    # Remove accents (combining diacritical marks)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def compute_minhash(text, ngram_length, num_hashes, a_list, b_list, mod):
    words = text.split()
    ngrams = set()
    for i in range(len(words) - ngram_length + 1):
        ngram = tuple(words[i:i + ngram_length])
        ngram_str = ' '.join(ngram)
        ngrams.add(ngram_str)
    
    if not ngrams:
        return [mod] * num_hashes
    
    signature = [mod] * num_hashes
    for ngram_str in ngrams:
        ngram_bytes = ngram_str.encode('utf-8')
        base_hash = int.from_bytes(hashlib.sha1(ngram_bytes).digest()[:8], byteorder='big') % mod
        for i in range(num_hashes):
            h_val = (a_list[i] * base_hash + b_list[i]) % mod
            if h_val < signature[i]:
                signature[i] = h_val
    return signature

def fuzzy_deduplicate(input_paths, num_hashes, num_bands, ngram_length, output_dir, jaccard_threshold):
    mod = 2**64
    a_list = [random.randint(1, mod-1) for _ in range(num_hashes)]
    b_list = [random.randint(0, mod-1) for _ in range(num_hashes)]
    
    original_contents = {}
    normalized_contents = {}
    for path in input_paths:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        original_contents[path] = content
        normalized_contents[path] = normalize_text(content)
    
    minhash_signatures = {}
    for path in input_paths:
        minhash_signatures[path] = compute_minhash(
            normalized_contents[path], ngram_length, num_hashes, a_list, b_list, mod
        )
    
    rows_per_band = num_hashes // num_bands
    lsh_buckets = defaultdict(list)
    for path in input_paths:
        sig = minhash_signatures[path]
        for band_idx in range(num_bands):
            start = band_idx * rows_per_band
            end = start + rows_per_band
            band_tuple = tuple(sig[start:end])
            bucket_key = (band_idx, band_tuple)
            lsh_buckets[bucket_key].append(path)
    
    candidate_pairs = set()
    for bucket in lsh_buckets.values():
        if len(bucket) > 1:
            sorted_bucket = sorted(bucket)
            for i in range(len(sorted_bucket)):
                for j in range(i+1, len(sorted_bucket)):
                    candidate_pairs.add((sorted_bucket[i], sorted_bucket[j]))
    
    graph = defaultdict(set)
    for path1, path2 in candidate_pairs:
        count = 0
        for i in range(num_hashes):
            if minhash_signatures[path1][i] == minhash_signatures[path2][i]:
                count += 1
        sim = count / num_hashes
        if sim >= jaccard_threshold:
            graph[path1].add(path2)
            graph[path2].add(path1)
    
    visited = set()
    components = []
    def dfs(node, graph, visited, comp):
        stack = [node]
        visited.add(node)
        while stack:
            current = stack.pop()
            comp.add(current)
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

    for node in graph:
        if node in visited:
            continue
        comp = set()
        dfs(node, graph, visited, comp)
        components.append(comp)
    
    keep_set = set()
    for comp in components:
        chosen = random.choice(list(comp))
        keep_set.add(chosen)
    
    all_paths = set(input_paths)
    non_duplicate_paths = all_paths - set(graph.keys())
    keep_set.update(non_duplicate_paths)
    
    os.makedirs(output_dir, exist_ok=True)
    for path in keep_set:
        basename = os.path.basename(path)
        output_path = os.path.join(output_dir, basename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(original_contents[path])
