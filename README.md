# care-review

C.A.R.E. messaging review — evaluate customer-facing messages for quality and engagement.

Zero dependencies. Python 3.11+.

## Install

```bash
pip install care-review
```

Or from source:

```bash
git clone https://github.com/kastrah/care-review.git
cd care-review
pip install -e .
```

## Python API

```python
from care import CAREReview

review = CAREReview()
result = review.evaluate("I'll fix this by Friday. Which time works best?")
print(result["verdict"])  # "ready to send"
```

### Return Structure

```python
{
    "C": {"pass": True, "issues": [], "fix": "..."},
    "A": {"pass": True, "issues": [], "fix": "..."},
    "R": {"pass": True, "issues": [], "fix": "..."},
    "E": {"pass": True, "issues": [], "fix": "..."},
    "verdict": "ready to send" | "needs fixes",
    "original": "..."
}
```

## CLI

```bash
# Review from stdin
echo "Your message here" | care-review

# Review from file
care-review --input message.txt

# JSON output
echo "Your message here" | care-review --output json

# Markdown output (default)
care-review --input message.txt --output md
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--input FILE`, `-i FILE` | Input file path. Use `-` or omit for stdin. |
| `--stdin` | Read input from stdin. |
| `--output {json,md}`, `-o` | Output format. Default: `md`. |

## C.A.R.E. Framework

- **C — Conversational**: Detects passive voice, corporate "we", generic appreciation, stiff phrasing
- **A — Actionable**: Detects vague timelines, empty CTAs, missing next steps
- **R — Richer than Asked**: Detects pure pitches, minimal answers without value-add
- **E — Engaging Dialogue**: Detects passive closings, missing reply paths

## License

MIT
