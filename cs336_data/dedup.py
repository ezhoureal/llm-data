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