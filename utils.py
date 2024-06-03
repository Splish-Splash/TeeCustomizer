from __future__ import annotations

import os
import re
import logging


def get_faq(filepath: str | os.PathLike) -> list[str]:
    if not os.path.exists(filepath):
        logging.error('Filepath %s does not exist', filepath)
        return []

    with open(filepath, 'r') as f:
        lines = f.readlines()

    qa_pairs = []
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            qa_pairs.append(line)
        elif line.startswith('A:'):
            qa_pairs[-1] += '\n' + line

    return qa_pairs
