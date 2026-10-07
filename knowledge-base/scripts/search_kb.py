#!/usr/bin/env python3
"""
Knowledge Base Search Script
Searches through local markdown and text files for relevant content.

Usage: python search_kb.py "<query>" "<knowledge_dir>"
"""

import sys
import os
import re
from pathlib import Path

# Force UTF-8 output so Chinese content is not garbled when captured by the gateway
sys.stdout.reconfigure(encoding='utf-8')


def search_files(query: str, knowledge_dir: str, max_results: int = 5) -> list:
    """Search through knowledge files for content matching the query."""
    query_lower = query.lower()
    query_terms = query_lower.split()
    results = []
    kb_path = Path(knowledge_dir)

    if not kb_path.exists():
        print(f"[ERROR] Knowledge directory not found: {knowledge_dir}")
        sys.exit(1)

    supported_extensions = {'.md', '.txt'}
    files = [f for f in kb_path.iterdir()
             if f.is_file() and f.suffix.lower() in supported_extensions]

    if not files:
        print("[INFO] No knowledge files found in the directory.")
        sys.exit(0)

    for filepath in sorted(files):
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"[WARN] Could not read {filepath.name}: {e}")
            continue

        content_lower = content.lower()

        # Count how many query terms appear in the content
        matched_terms = [t for t in query_terms if t in content_lower]
        term_score = len(matched_terms) / len(query_terms) if query_terms else 0

        # Check for exact phrase match (higher priority)
        exact_match = query_lower in content_lower
        exact_score = 1.0 if exact_match else 0.0

        score = exact_score * 0.6 + term_score * 0.4

        if score > 0:
            # Extract the most relevant paragraph/section
            relevant_excerpt = extract_relevant_excerpt(content, query_lower)
            results.append({
                'file': filepath.name,
                'path': str(filepath),
                'score': score,
                'excerpt': relevant_excerpt
            })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:max_results]


def extract_relevant_excerpt(content: str, query_lower: str, context_chars: int = 300) -> str:
    """Extract the most relevant excerpt around the query match."""
    idx = content.lower().find(query_lower)
    if idx == -1:
        # Return first 300 chars as fallback
        return content[:context_chars].strip()

    start = max(0, idx - context_chars // 2)
    end = min(len(content), idx + context_chars // 2)

    # Try to align to paragraph boundaries
    if start > 0:
        para_start = content.rfind('\n\n', 0, start)
        if para_start != -1:
            start = para_start + 2

    if end < len(content):
        para_end = content.find('\n\n', end)
        if para_end != -1:
            end = para_end

    excerpt = content[start:end].strip()
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(content):
        excerpt = excerpt + "..."

    return excerpt


def main():
    if len(sys.argv) < 3:
        print("Usage: python search_kb.py \"<query>\" \"<knowledge_dir>\"")
        sys.exit(1)

    query = sys.argv[1]
    knowledge_dir = sys.argv[2]

    results = search_files(query, knowledge_dir)

    if not results:
        print(f"[NO_RESULTS] No relevant content found for query: {query}")
        sys.exit(0)

    for i, r in enumerate(results, 1):
        print(f"=== Result {i} (score: {r['score']:.2f}) ===")
        print(f"File: {r['file']}")
        print(f"Path: {r['path']}")
        print(f"---")
        print(r['excerpt'])
        print(f"=== End Result {i} ===\n")


if __name__ == '__main__':
    main()
