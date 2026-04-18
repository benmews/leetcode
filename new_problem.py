#!/usr/bin/env python3
"""Creates a new LeetCode problem folder and pre-fills solution/test stubs.

Usage:   python new_problem.py              # today's daily challenge (Python)
         python new_problem.py --cpp        # today's daily challenge (Python + C++)
         python new_problem.py <number>     # specific problem (Python)
         python new_problem.py <number> --cpp   # specific problem (Python + C++)
         python new_problem.py --cpp <number>   # specific problem (Python + C++)
         python new_problem.py --cpp <number>   # add C++ to existing folder
Example: python new_problem.py 3740
         python new_problem.py 3783 --cpp
"""

import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PROBLEMS_DIR = ROOT / "problems"

LC_PROBLEMS_API = "https://leetcode.com/api/problems/all/"
LC_GRAPHQL = "https://leetcode.com/graphql"

# Python type map
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

# C++ type map (for test value conversion only; solution uses the API snippet)
CPP_TYPE_MAP = {
    "integer": "int",
    "integer[]": "vector<int>",
    "integer[][]": "vector<vector<int>>",
    "string": "string",
    "string[]": "vector<string>",
    "string[][]": "vector<vector<string>>",
    "boolean": "bool",
    "double": "double",
    "long": "long long",
    "long[]": "vector<long long>",
    "character": "char",
    "character[]": "vector<char>",
    "void": "void",
}

COMMON_CPP_INCLUDES = """\
#include <algorithm>
#include <numeric>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
"""


def lc_to_py(lc_type: str) -> str:
    return TYPE_MAP.get(lc_type, "Any")


def lc_to_cpp(lc_type: str) -> str:
    return CPP_TYPE_MAP.get(lc_type, "auto")


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


def get_daily() -> tuple[int, str, str]:
    """Return (number, slug, title) for today's daily challenge."""
    print("Fetching today's daily challenge ...")
    query = """
    query {
      activeDailyCodingChallengeQuestion {
        question {
          questionFrontendId
          titleSlug
          title
        }
      }
    }
    """
    payload = json.dumps({"query": query}).encode()
    q = fetch(LC_GRAPHQL, payload)["data"]["activeDailyCodingChallengeQuestion"]["question"]
    return int(q["questionFrontendId"]), q["titleSlug"], q["title"]


def get_details(slug: str) -> dict:
    print(f"Fetching details for '{slug}' ...")
    query = """
    query details($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty
        content
        exampleTestcaseList
        metaData
        codeSnippets {
          langSlug
          code
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"titleSlug": slug}}).encode()
    return fetch(LC_GRAPHQL, payload)["data"]["question"]


def extract_outputs(raw_html: str) -> list[str]:
    """Pull expected output values from the HTML problem description.

    Handles two formats used by LeetCode:
      <strong>Output:</strong> 42
      <strong>Output:</strong> <span class="example-io">42</span>
    """
    results = []
    for m in re.finditer(r"<strong>Output:</strong>\s*(?:<[^>]+>)?([^<\n]+)", raw_html):
        results.append(m.group(1).strip())
    return results


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


def build_solution_py(number: int, title: str, slug: str, meta: dict) -> str:
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


def build_tests_py(
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


def to_cpp_literal(raw: str, cpp_type: str, typed: bool = False) -> str:
    """Convert a raw LeetCode value string to a C++ literal.

    typed=True wraps vector literals with their type name, needed for the
    expected-value side of assertions (implicit conversion doesn't apply there).
    """
    raw = raw.strip()
    if "vector" in cpp_type:
        inner = raw.replace("[", "{").replace("]", "}")
        return f"{cpp_type}{inner}" if typed else inner
    if cpp_type == "bool":
        return raw.lower()  # Python True/False -> C++ true/false
    return raw


def build_solution_cpp(number: int, title: str, slug: str, snippet: str) -> str:
    return (
        f"// {number}. {title}\n"
        f"// https://leetcode.com/problems/{slug}/\n\n"
        f"{COMMON_CPP_INCLUDES}\n"
        f"{snippet}\n"
    )


def build_tests_cpp(
    meta: dict, example_inputs: list[str], example_outputs: list[str]
) -> str:
    func = meta.get("name", "solve")
    params = meta.get("params", [])
    ret_cpp = lc_to_cpp(meta.get("return", {}).get("type", "auto"))

    lines = [
        '#include "solution.cpp"\n',
        "#include <cassert>\n",
        "#include <iostream>\n",
        "\n",
        "int main() {\n",
        "    Solution s;\n",
    ]

    for i, raw_input in enumerate(example_inputs, 1):
        args = raw_input.splitlines()
        if len(args) == len(params):
            cpp_args = ", ".join(
                to_cpp_literal(args[j], lc_to_cpp(params[j]["type"]))
                for j in range(len(params))
            )
        else:
            cpp_args = ", ".join(args)

        lines.append(f"\n    // Example {i}\n")
        if i - 1 < len(example_outputs):
            expected = to_cpp_literal(example_outputs[i - 1], ret_cpp, typed=True)
            lines.append(f'    assert(s.{func}({cpp_args}) == {expected});\n')
        else:
            lines.append(f'    // assert(s.{func}({cpp_args}) == /* expected */);\n')
        lines.append(f'    std::cout << "test_example_{i} PASSED\\n";\n')

    lines += [
        '\n    std::cout << "\\nAll tests passed!\\n";\n',
        "    return 0;\n",
        "}\n",
    ]

    return "".join(lines)


def open_in_vscode(paths: list[Path]) -> None:
    existing = [str(p) for p in paths if p.exists()]
    try:
        subprocess.run(["code", "--reuse-window"] + existing, check=True)
    except FileNotFoundError:
        print("\n  (VS Code 'code' CLI not found — open the files manually)")


def main() -> None:
    raw_args = sys.argv[1:]
    cpp = "--cpp" in raw_args
    args = [a for a in raw_args if a != "--cpp"]

    if len(args) == 0:
        number, slug, title = get_daily()
    elif len(args) == 1 and args[0].isdigit():
        number = int(args[0])
        slug, title = get_slug(number)
    else:
        print(__doc__)
        sys.exit(1)

    details = get_details(slug)

    meta = json.loads(details.get("metaData") or "{}")
    example_inputs: list[str] = details.get("exampleTestcaseList") or []
    content: str = details.get("content") or ""
    example_outputs = extract_outputs(content)
    difficulty = details.get("difficulty", "")

    folder = PROBLEMS_DIR / f"p{number}_{slug.replace('-', '_')}"
    folder_exists = folder.exists()

    if folder_exists and not cpp:
        raise SystemExit(f"Folder already exists: {folder.relative_to(ROOT)}/")

    files_created: list[Path] = []

    if not folder_exists:
        folder.mkdir()
        (folder / "__init__.py").write_text("")

        py_solution = folder / "solution.py"
        py_tests = folder / "test_solution.py"
        py_solution.write_text(build_solution_py(number, title, slug, meta))
        py_tests.write_text(build_tests_py(meta, example_inputs, example_outputs))
        files_created += [py_solution, py_tests]

        if content:
            problem_md = folder / "problem.md"
            problem_md.write_text(build_problem(number, title, slug, difficulty, content))
            files_created.insert(0, problem_md)

    if cpp:
        snippets = {s["langSlug"]: s["code"] for s in (details.get("codeSnippets") or [])}
        cpp_snippet = snippets.get("cpp", f"class Solution {{\npublic:\n    // TODO\n}};\n")

        cpp_solution = folder / "solution.cpp"
        cpp_tests = folder / "test_solution.cpp"

        if cpp_solution.exists():
            raise SystemExit(f"C++ files already exist in {folder.relative_to(ROOT)}/")

        cpp_solution.write_text(build_solution_cpp(number, title, slug, cpp_snippet))
        cpp_tests.write_text(build_tests_cpp(meta, example_inputs, example_outputs))
        files_created += [cpp_solution, cpp_tests]

    # Summary
    outputs_note = (
        "expected outputs extracted"
        if example_outputs
        else "fill in expected outputs"
    )
    action = "Added C++ to" if (folder_exists and cpp) else "Created"
    print(f"\n{action}: {number}. {title}  [{difficulty}]")
    print(f"  {folder.relative_to(ROOT)}/")
    for f in files_created:
        print(f"    {f.name}")
    print(f"  ({len(example_inputs)} example test(s), {outputs_note})")
    print(f"\n  https://leetcode.com/problems/{slug}/")

    open_in_vscode(files_created)


if __name__ == "__main__":
    main()
