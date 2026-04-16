#!/usr/bin/env python3
"""Creates a new LeetCode problem folder and pre-fills solution/test stubs.

Usage:   python new_problem.py <problem_number>
Example: python new_problem.py 3740
"""

import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PROBLEMS_DIR = ROOT / "problems"

LC_PROBLEMS_API = "https://leetcode.com/api/problems/all/"
LC_GRAPHQL = "https://leetcode.com/graphql"

TYPE_MAP = {
    "integer": "int",
    "integer[]": "List[int]",
    "integer[][]": "List[List[int]]",
    "string": "str",
    "string[]": "List[str]",
    "string[][]": "List[List[str]]",
    "boolean": "bool",
    "double": "float",
    "long": "int",
    "long[]": "List[int]",
    "character": "str",
    "character[]": "List[str]",
    "void": "None",
}


def lc_to_py(lc_type: str) -> str:
    return TYPE_MAP.get(lc_type, "Any")


def fetch(url: str, payload: bytes | None = None) -> dict:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://leetcode.com",
    }
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} when fetching {url}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e.reason}") from e


def get_slug(number: int) -> tuple[str, str]:
    print("Fetching problem list ...")
    data = fetch(LC_PROBLEMS_API)
    for item in data["stat_status_pairs"]:
        stat = item["stat"]
        if stat["frontend_question_id"] == number:
            return stat["question__title_slug"], stat["question__title"]
    raise SystemExit(f"Problem #{number} not found.")


def get_details(slug: str) -> dict:
    print(f"Fetching details for '{slug}' ...")
    query = """
    query details($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty
        content
        exampleTestcaseList
        metaData
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"titleSlug": slug}}).encode()
    return fetch(LC_GRAPHQL, payload)["data"]["question"]


def extract_outputs(html: str) -> list[str]:
    """Pull expected output values from the HTML problem description."""
    return [
        m.group(1).strip()
        for m in re.finditer(r"<strong>Output:</strong>\s*([^<\n]+)", html)
    ]


def html_to_md(raw: str) -> str:
    """Convert LeetCode HTML description to plain Markdown."""
    s = raw

    # Code blocks: <pre>...</pre>
    s = re.sub(
        r"<pre>\s*(.*?)\s*</pre>",
        lambda m: "```\n" + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "\n```",
        s, flags=re.DOTALL,
    )

    # Headings
    for lvl in range(1, 7):
        s = re.sub(rf"<h{lvl}[^>]*>(.*?)</h{lvl}>", r"\1\n" + "=" * 20, s, flags=re.DOTALL)

    # Inline formatting
    s = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", s, flags=re.DOTALL)
    s = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", s, flags=re.DOTALL)
    s = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", s, flags=re.DOTALL)
    s = re.sub(r"<sup[^>]*>(.*?)</sup>", r"^\1", s, flags=re.DOTALL)
    s = re.sub(r"<sub[^>]*>(.*?)</sub>", r"_\1", s, flags=re.DOTALL)

    # Lists
    s = re.sub(r"<li[^>]*>\s*(.*?)\s*</li>", r"- \1", s, flags=re.DOTALL)
    s = re.sub(r"</?(ul|ol)[^>]*>", "", s)

    # Paragraphs / line breaks
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"<p[^>]*>&nbsp;</p>", "", s)  # blank spacer paragraphs
    s = re.sub(r"<p[^>]*>", "", s)

    # Strip remaining tags
    s = re.sub(r"<[^>]+>", "", s)

    # HTML entities
    s = html.unescape(s)

    # Strip leading whitespace from each line outside code fences
    cleaned: list[str] = []
    in_fence = False
    for line in s.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        cleaned.append(line if in_fence else line.lstrip())
    s = "\n".join(cleaned)

    # Collapse excessive blank lines
    s = re.sub(r"\n{3,}", "\n\n", s)

    return s.strip()


def build_problem(number: int, title: str, slug: str, difficulty: str, content: str) -> str:
    md = html_to_md(content) if content else "*(description not available)*"
    return (
        f"# {number}. {title}  [{difficulty}]\n"
        f"<https://leetcode.com/problems/{slug}/>\n\n"
        f"{md}\n"
    )


def build_solution(number: int, title: str, slug: str, meta: dict) -> str:
    func = meta.get("name", "solve")
    params = meta.get("params", [])
    ret = lc_to_py(meta.get("return", {}).get("type", "Any"))

    needed: set[str] = set()
    param_parts: list[str] = []
    for p in params:
        py_t = lc_to_py(p["type"])
        if "List" in py_t:
            needed.add("List")
        if "Any" in py_t:
            needed.add("Any")
        param_parts.append(f"{p['name']}: {py_t}")
    if "List" in ret:
        needed.add("List")
    if "Any" in ret:
        needed.add("Any")

    import_line = (
        f"from typing import {', '.join(sorted(needed))}\n\n\n" if needed else ""
    )

    return (
        f"# {number}. {title}\n"
        f"# https://leetcode.com/problems/{slug}/\n\n"
        f"{import_line}"
        f"class Solution:\n"
        f"    def {func}(self, {', '.join(param_parts)}) -> {ret}:\n"
        f"        pass\n"
    )


def build_tests(
    meta: dict, example_inputs: list[str], example_outputs: list[str]
) -> str:
    func = meta.get("name", "solve")
    params = meta.get("params", [])
    lines = ["from .solution import Solution\n"]

    for i, raw_input in enumerate(example_inputs, 1):
        args = raw_input.splitlines()
        if len(args) == len(params):
            arg_str = ", ".join(
                f"{params[j]['name']}={args[j]}" for j in range(len(params))
            )
        else:
            arg_str = ", ".join(args)
        expected = example_outputs[i - 1] if i - 1 < len(example_outputs) else "..."
        lines.append(
            f"\n\ndef test_example_{i}():\n"
            f"    assert Solution().{func}({arg_str}) == {expected}\n"
        )

    return "".join(lines)


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print(__doc__)
        sys.exit(1)

    number = int(sys.argv[1])
    slug, title = get_slug(number)
    details = get_details(slug)

    meta = json.loads(details.get("metaData") or "{}")
    example_inputs: list[str] = details.get("exampleTestcaseList") or []
    content: str = details.get("content") or ""
    example_outputs = extract_outputs(content)

    folder = PROBLEMS_DIR / f"{slug.replace('-', '_')}_{number}"
    if folder.exists():
        raise SystemExit(f"Folder already exists: {folder.relative_to(ROOT)}/")

    difficulty = details.get("difficulty", "")

    folder.mkdir()
    (folder / "__init__.py").write_text("")
    (folder / "solution.py").write_text(build_solution(number, title, slug, meta))
    (folder / "test_solution.py").write_text(
        build_tests(meta, example_inputs, example_outputs)
    )
    if content:
        (folder / "problem.md").write_text(build_problem(number, title, slug, difficulty, content))

    outputs_note = (
        "expected outputs extracted automatically"
        if example_outputs
        else "fill in expected outputs — marked with '...'"
    )
    print(f"\n{number}. {title}  [{difficulty}]")
    print(f"  {folder.relative_to(ROOT)}/")
    print(f"    problem.md" if content else "    problem.md  (not available)")
    print(f"    solution.py")
    print(f"    test_solution.py  ({len(example_inputs)} example test(s), {outputs_note})")
    print(f"\n  https://leetcode.com/problems/{slug}/")


if __name__ == "__main__":
    main()
