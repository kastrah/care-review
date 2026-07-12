# care-review

C.A.R.E. is a messaging review framework that checks whether a customer-facing message sounds like a person wrote it, gives the reader something useful, and ends with a reason to reply.

You can use it three ways: as a skill that an AI agent follows when reviewing messages, as a command-line tool you run from your terminal, or as a Python library you import into your own code. Zero dependencies. Python 3.11+.

## What C.A.R.E. checks

Every message is tested against four principles:

- **C — Conversational**: Does this sound like a person speaking to one person, or a brand speaking at an audience?
- **A — Actionable**: After reading once, does the reader know what happens next and when?
- **R — Richer than Asked**: Did the message give the reader something useful before asking for anything?
- **E — Engaging Dialogue**: Does the ending create a specific reason for the reader to reply?

Each principle passes or fails. Failures come with a one-line fix direction. No rewrites by default — just the issue and where to point the correction.

## Why this matters

Most messages that go out of customer-facing teams fail on at least one of these principles without anyone noticing. The email sounds fine when you write it, but the reader finishes it and has no idea what happens next. The WhatsApp response answers the question but gives nothing extra, so the customer never comes back. The complaint reply is technically correct but reads like it was written by a system, not a person.

C.A.R.E. catches these problems before the message goes out. It is fast enough to run on every outbound message and specific enough to tell you exactly what to fix.

## Use cases

### Customer support responses

A customer writes in about a delayed delivery. The agent drafts a reply that confirms the delay and apologises. C.A.R.E. flags that the reply has no next step — the customer does not know when to expect an update, or who to contact if it happens again. The fix: add a timeline and a name.

### Complaint handling

A customer is angry about a billing error. The draft response explains the error and promises a refund. C.A.R.E. flags that the message does not acknowledge the frustration before jumping to the fix. The R (Richer than Asked) principle fails because the reader gets the fix but nothing that shows they were heard.

### WhatsApp and SMS

A pharmacy sends a refill reminder via WhatsApp. The message says "Your medication is ready for pickup." C.A.R.E. flags that there is no deadline, no alternative if they cannot come in, and no reason to reply. The fix: add a pickup window, a delivery option, and a question that moves the conversation forward.

### Outbound sales and follow-up

A sales rep sends a follow-up email after a demo. The email recaps the product features and asks for a meeting. C.A.R.E. flags that the email leads with what the product does instead of what the prospect gets. The A (Actionable) principle fails because "let me know when you're free" is not a clear next step.

### Retention messages

A customer wants to cancel. The agent drafts a response that processes the cancellation. C.A.R.E. flags that before processing, the message should surface what the customer stands to lose — not to block the cancellation, but to make sure the decision is informed.

### Internal handoff messages

A team member sends a handoff message to a colleague about an open ticket. C.A.R.E. flags that the message does not name what already happened, what needs to happen next, and by when. The fix: add the timeline, the owner, and the specific action required.

## How it fits with other tools

This tool is part of a three-skill writing stack. Each tool does one job well.

| Tool | What it does | When to use it |
|------|-------------|----------------|
| [copy-pass](https://github.com/kastrah/copy-pass) | Strengthens persuasion: hooks, CTAs, objections, emotional triggers, platform fit | Before a senior writer reviews copy. Not for final cleanup. |
| care-review | Checks whether a message is conversational, actionable, richer than asked, and ends with a reason to reply | Before any customer-facing message goes out. |
| [humaniser](https://github.com/kastrah/humaniser) | Removes AI writing patterns and makes text sound natural | After copy pass. Final voice pass before publishing. |

### If you are on care-review but need something else

- **Your copy needs stronger hooks, CTAs, or persuasion structure** → use [copy-pass](https://github.com/kastrah/copy-pass)
- **Your copy sounds like AI wrote it** → use [humaniser](https://github.com/kastrah/humaniser)
- **You are writing a blog, landing page, or article** → start with [copy-pass](https://github.com/kastrah/copy-pass), then [humaniser](https://github.com/kastrah/humaniser)
- **You are writing an email, SMS, WhatsApp message, or complaint response** → start here with care-review

## Workflows

### Customer-facing message (email, SMS, WhatsApp, complaint response)

```text
Draft → care-review → revise → send
```

Run care-review before sending. If the message also needs persuasion work (launch email, promotional SMS), run copy-pass first:

```text
Draft → copy-pass → care-review → revise → send
```

### Content for a general audience (blog, landing page, social post, article)

```text
Research → Draft → copy-pass → humaniser → final review → publish
```

humaniser handles the AI-tell cleanup. copy-pass handles the persuasion structure. care-review handles the conversational check — it applies wherever the text needs to sound like a person talking to a person, regardless of audience size.

### Campaign with both content and direct messages

```text
Content:  Draft → copy-pass → humaniser → publish
Messages: Draft → care-review → send
```

Run the content and message tracks separately. The content track ends with humaniser. The message track ends with care-review. They converge at publish.

## Install

### Claude Code

```bash
git clone https://github.com/kastrah/care-review.git ~/.claude/skills/care-review
```

### OpenCode / Codex CLI

Place `SKILL.md` in your project root or globally at `~/.config/opencode/AGENTS.md`.

### Python package

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

### Return structure

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

### CLI options

| Option | Description |
|--------|-------------|
| `--input FILE`, `-i FILE` | Input file path. Use `-` or omit for stdin. |
| `--stdin` | Read input from stdin. |
| `--output {json,md}`, `-o` | Output format. Default: `md`. |

## License

MIT
