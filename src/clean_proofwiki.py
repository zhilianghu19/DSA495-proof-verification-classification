"""Extract conservative theorem–proof pairs from NaturalProofs ProofWiki JSON."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from tempfile import NamedTemporaryFile


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = REPO_ROOT / "Data" / "naturalproofs_proofwiki.json"
CLEAN_FILE = REPO_ROOT / "Data" / "naturalproofs_proofwiki_clean.json"

COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
MATH_SLOT = re.compile(r"\x00([0-9]+)\x00")
CATEGORY_LINE = re.compile(r"(?im)^[ \t]*\[\[Category:[^\[\]\n]+\]\][ \t]*$")
NESTED_EQUATION = re.compile(r"\{\{\s*eqn\s*\|(?:(?!\{\{|\}\})[\s\S])*\{\{", re.I)
REVISION_TRAILER = re.compile(
    r"(?im)(?<=\n)[ \t]*[a-z0-9]{31}[ \t]*\s*\Z"
)
INTERNAL_LINK = re.compile(r"\[\[([^\[\]]+)\]\]")
EXTERNAL_LINK = re.compile(
    r"\[((?:https?:)?//[^\s|\]]+)(?:[ \t]+\|?[ \t]*|\|)?([^\]\n]*)\]",
    re.IGNORECASE,
)
RAW_URL = re.compile(r"https?://[^\s<>\]]+|(?<!\w)www\.[^\s<>\]]+", re.IGNORECASE)
MEDIA_LINK = re.compile(r"\[\[\s*:?(?:file|image|media)\s*:", re.IGNORECASE)
INCOMPLETE_TEMPLATE = re.compile(
    r"\{\{\s*(?:proof\s*wanted|finish|wip|stub|hand\s*waving|"
    r"questionable|mistake|explain|expand|rewrite|proofread|improve)\s*(?=[|}])",
    re.IGNORECASE,
)
REFERENCE_ONLY = re.compile(
    r"\A\s*(?:see\s+(?:the\s+)?proof\b|"
    r"(?:the|a) proof (?:of this theorem )?(?:can be found|is (?:omitted|given elsewhere)|"
    r"is beyond the (?:current )?scope)|"
    r"(?:the\s+)?(?:proof|details) (?:is |are )?left as an exercise)",
    re.IGNORECASE,
)
SHORT_REFERENCE = re.compile(
    r"\A(?:by|from|see|refer to|immediate from|(?:this |the result )?follows "
    r"(?:directly |immediately )?from|this is (?:an? |the )?(?:immediate )?"
    r"(?:corollary|special case))\b",
    re.IGNORECASE,
)
CITATION_LIST_LEAD = re.compile(
    r"(?:the result )?(?:this )?(?:follows (?:directly |immediately )?from|"
    r"immediate(?:ly)? from|see|refer to)\s*:",
    re.IGNORECASE,
)
CITATION_LIST_ENTRY = re.compile(r"^[ \t]*[:*#]*[ \t]*.*\[\[[^\n]+?\]\][.!;]?[ \t]*$")
PROOF_END = re.compile(r"\{\{\s*qed\s*\}\}", re.IGNORECASE)
INCOMPLETE_PROSE = re.compile(
    r"\b(?:proof (?:is )?(?:missing|incomplete|under construction)|"
    r"(?:the )?proof (?:is )?to be (?:added|written|completed)|"
    r"(?:details|proof) (?:is |are )?(?:left as an exercise|omitted))\b",
    re.IGNORECASE,
)
WIKI_TEMPLATE = re.compile(r"\{\{((?:[^{}]|\{(?!\{)|\}(?!\}))*?)\}\}")
HEADING = re.compile(r"^\s*(={2,6})\s*(.*?)\s*\1\s*$", re.MULTILINE)
UNSUPPORTED_MARKUP = re.compile(
    r"\{\{|\[\[|\]\]|<!--|^[ \t]*(?:\{\||\|-|\|\}|! )|"
    r"</?[A-Za-z][A-Za-z0-9-]*(?:[ \t][^<>\n]*)?/?>",
    re.IGNORECASE | re.MULTILINE,
)
MATH_DELIMITER = re.compile(r"\\(?:[\\$]|[()[\]])|\$\$?")
MATH_BRACE = re.compile(r"\\(?:[\\{}])|[{}]")
PROSE_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
MIN_PROSE_WORDS = 15

SIMPLE_TEMPLATES = {
    "iff": "if and only if",
    "lhs": "left-hand side",
    "rhs": "right-hand side",
    "wlog": "without loss of generality",
    "wrt": "with respect to",
}
FORMATTING_TEMPLATES = {"begin-eqn", "end-eqn", "qed"}
EQN_COLUMNS = ("l", "o", "r")
EQN_KEYS = {*EQN_COLUMNS, "n", "c"}


class SkipRecord(Exception):
    """The source record cannot be extracted without guessing."""


def link_text(match):
    target, separator, label = match[1].partition("|")
    target = target.strip()
    if not re.search(r"[A-Za-z]{2}", target):
        raise SkipRecord("ambiguous_wiki_link")
    if target.casefold().startswith("category:"):
        raise SkipRecord("inline_category_tag")
    if separator:
        if not label.strip() or "|" in label:
            raise SkipRecord("ambiguous_wiki_link")
        return label.strip()
    return target.removeprefix(":")


def heading_text(match):
    heading = match[2].strip()
    if not re.search(r"[A-Za-z]{3}", heading) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9 '()-]*", heading):
        raise SkipRecord("ambiguous_heading")
    return heading


def render_equation(args):
    fields = {}
    for arg in args:
        key, separator, value = arg.partition("=")
        key = key.strip()
        if not separator or key not in EQN_KEYS or key in fields:
            raise SkipRecord("unsupported_equation")
        fields[key] = value.strip()

    if not fields.get("r") or (fields.get("l") and fields.get("o") == ""):
        raise SkipRecord("unsupported_equation")
    fields.setdefault("o", "=")

    equation = " ".join(fields[key] for key in EQN_COLUMNS if fields.get(key))
    if "$" in equation or "\x00" in equation or equation.endswith("="):
        raise SkipRecord("unsupported_equation")
    label = fields.get("n", "")
    if label and not re.fullmatch(r"[A-Za-z0-9]+", label):
        raise SkipRecord("unsupported_equation")
    line = f"({label}) " if label else ""
    line += f"$${equation}$$"
    if fields.get("c"):
        line += "\n" + fields["c"]
    return line


def render_template(match):
    raw_name, *args = match[1].split("|")
    name = raw_name.strip().replace("_", " ").casefold()
    if name == "eqn":
        return render_equation(args)
    if not args and name in SIMPLE_TEMPLATES:
        return SIMPLE_TEMPLATES[name]
    if not args and name in FORMATTING_TEMPLATES:
        return ""
    if name in {"eqn-title", "eqn-intertext"} and len(args) == 1 and args[0].strip():
        return args[0].strip()
    if name == "defof" and args and args[0].strip():
        page = args[0].strip()
        if len(args) == 1:
            return f"definition of {page}"
        if len(args) == 2 and re.fullmatch(r"index\s*=\s*\d+", args[1].strip()):
            return f"definition of {page} (definition {args[1].split('=', 1)[1].strip()})"
    raise SkipRecord("unsupported_wiki_template")


def math_segments(text):
    """Yield prose and delimited math separately while checking delimiters and braces."""
    closers = {"$": "$", "$$": "$$", r"\(": r"\)", r"\[": r"\]"}
    expected = None
    start = 0
    for match in MATH_DELIMITER.finditer(text):
        token = match[0]
        if token in {r"\$", r"\\"}:
            continue
        if expected is None:
            if token not in closers:
                raise SkipRecord("unbalanced_math")
            yield False, text[start:match.start()]
            opening = match
            expected = closers[token]
            continue
        if token != expected:
            raise SkipRecord("unbalanced_math")
        depth = 0
        for brace in MATH_BRACE.finditer(text, opening.end(), match.start()):
            depth += (brace[0] == "{") - (brace[0] == "}")
            if depth < 0:
                raise SkipRecord("unbalanced_math")
        if depth:
            raise SkipRecord("unbalanced_math")
        yield True, text[opening.start():match.end()]
        start = match.end()
        expected = None
    if expected is not None:
        raise SkipRecord("unbalanced_math")
    yield False, text[start:]


def prose_without_math(text):
    return " ".join(segment for is_math, segment in math_segments(text) if not is_math)


def explicit_math(text):
    for is_math, segment in math_segments(text):
        if is_math:
            yield segment


def format_prose(text):
    if "''" in text:
        raise SkipRecord("ambiguous_prose_apostrophes")
    # Indentation immediately before an intact formula is recognizable. Leave
    # colons before ordinary text or operators (e.g. :=) alone.
    text = re.sub(r"(?m)^[ \t]*:+[ \t]*(?=\x00)", "", text)
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    return re.sub(r"\n{2,}", "\n", text)


def is_citation_list(text):
    lines = [line.strip() for line in COMMENT.sub("", text).splitlines() if line.strip()]
    lines = [line for line in lines if not PROOF_END.fullmatch(line)]
    return (
        len(lines) > 1
        and bool(CITATION_LIST_LEAD.fullmatch(lines[0]))
        and "$" not in text
        and all(CITATION_LIST_ENTRY.fullmatch(line) for line in lines[1:])
    )


def clean_text(text):
    if not text.strip():
        raise SkipRecord("empty_text")
    if "\x00" in text or "<!--" in text:
        raise SkipRecord("ambiguous_source_markup")
    original_math = []
    pieces = []
    for is_math, segment in math_segments(text):
        if is_math:
            if "[[" in segment or "{{" in segment or "<br" in segment.casefold():
                raise SkipRecord("markup_inside_math")
            pieces.append(f"\x00{len(original_math)}\x00")
            original_math.append(segment)
        else:
            pieces.append(segment)
    text = "".join(pieces)
    if INCOMPLETE_TEMPLATE.search(text) or INCOMPLETE_PROSE.search(text):
        raise SkipRecord("incomplete_source_text")
    if MEDIA_LINK.search(text):
        raise SkipRecord("requires_media")
    # A 31-character token alone could also be mathematical content. Remove
    # it only when it follows a standalone category in the export footer.
    trailer = REVISION_TRAILER.search(text)
    if trailer:
        preceding_line = text[:trailer.start()].rstrip().rsplit("\n", 1)[-1].strip()
        if not CATEGORY_LINE.fullmatch(preceding_line):
            raise SkipRecord("ambiguous_trailer")
        text = text[:trailer.start()]
    text = CATEGORY_LINE.sub("", text)
    text = INTERNAL_LINK.sub(link_text, text)
    text = EXTERNAL_LINK.sub(lambda match: match[2].strip(), text)
    if RAW_URL.search(text):
        raise SkipRecord("unresolved_url")
    if "{{{" in text or "}}}" in text or NESTED_EQUATION.search(text):
        raise SkipRecord("nested_equation_template")
    while "{{" in text:
        text, replacements = WIKI_TEMPLATE.subn(render_template, text)
        if not replacements:
            break
    text = re.sub(r"</?br\s*/?>", "\n", text, flags=re.IGNORECASE)
    if UNSUPPORTED_MARKUP.search(text):
        raise SkipRecord("unsupported_wiki_markup")
    text = HEADING.sub(heading_text, text)
    text = "".join(
        segment if is_math else format_prose(segment)
        for is_math, segment in math_segments(text)
    )
    text = text.strip()
    if MATH_SLOT.findall(text) != [str(index) for index in range(len(original_math))]:
        raise SkipRecord("changed_source_math")
    text = MATH_SLOT.sub(lambda match: original_math[int(match[1])], text)
    if not text:
        raise SkipRecord("empty_text")
    # Wiki equation templates can add display math. Original delimited formulas
    # must still appear in order, including their original whitespace.
    output_math = explicit_math(text)
    for formula in original_math:
        if not any(candidate == formula for candidate in output_math):
            raise SkipRecord("changed_source_math")
    return text


def body(record):
    lines = record.get("contents")
    if not isinstance(lines, list) or any(not isinstance(line, str) for line in lines):
        raise SkipRecord("missing_or_malformed_contents")
    return "\n".join(lines)


def extract_pairs(theorems, counts):
    for theorem in theorems:
        counts["source_theorems"] += 1
        proofs = theorem.get("proofs")
        if not isinstance(proofs, list) or not proofs:
            counts["theorems_without_proof"] += 1
            continue
        counts["source_proofs"] += len(proofs)
        try:
            statement = clean_text(body(theorem))
            title = clean_text(theorem["title"])
            prose_without_math(statement)
            prose_without_math(title)
        except SkipRecord as exc:
            counts[f"skipped_theorem_{exc}"] += len(proofs)
            continue
        seen_proofs = set()
        for proof in proofs:
            try:
                raw_proof = body(proof)
                if REFERENCE_ONLY.match(raw_proof) or is_citation_list(raw_proof):
                    raise SkipRecord("reference_only")
                proof_text = clean_text(raw_proof)
                prose = prose_without_math(proof_text)
                if REFERENCE_ONLY.match(prose) or (
                    "\n" not in proof_text and prose.strip() == proof_text
                    and SHORT_REFERENCE.match(proof_text)
                ):
                    raise SkipRecord("reference_only")
                if len(PROSE_WORD.findall(prose)) < MIN_PROSE_WORDS:
                    raise SkipRecord("too_little_prose")
                if proof_text in seen_proofs:
                    raise SkipRecord("duplicate_text")
            except SkipRecord as exc:
                counts[f"skipped_proof_{exc}"] += 1
                continue
            seen_proofs.add(proof_text)
            counts["kept_pairs"] += 1
            yield {
                "theorem_id": theorem["id"],
                "title": title,
                "theorem_text": statement,
                "proof_text": proof_text,
            }


def run(source, output):
    if source.resolve() == output.resolve() or (output.exists() and source.samefile(output)):
        raise ValueError("Input and output must be different files.")
    with source.open(encoding="utf-8-sig") as stream:
        theorems = json.load(stream)["dataset"]["theorems"]
    output.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=output.parent, delete=False
        ) as stream:
            temporary_path = Path(stream.name)
            stream.write("[\n")
            for index, record in enumerate(extract_pairs(theorems, counts)):
                if index:
                    stream.write(",\n")
                stream.write("  " + json.dumps(record, ensure_ascii=False))
            stream.write("\n]\n")
        temporary_path.replace(output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=RAW_FILE, help="path to the original ProofWiki JSON")
    parser.add_argument("--output", type=Path, default=CLEAN_FILE)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"original ProofWiki JSON not found at {args.input}; pass its location with --input")
    counts = run(args.input, args.output)
    print(json.dumps(dict(sorted(counts.items())), indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
