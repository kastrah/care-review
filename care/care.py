"""C.A.R.E. message review engine.

Evaluates customer-facing messages against the C.A.R.E. framework:
  C — Conversational
  A — Actionable
  R — Richer than Asked
  E — Engaging Dialogue
"""

import re
from typing import Dict, List

from care.base import PrincipleResult


class CAREReview:
    """Evaluate customer-facing messages against the C.A.R.E. framework."""

    _PASSIVE_RE = re.compile(
        r"\b(?:has been|will be|is being|was|were|been|be|is|are)\s+\w+ed\b",
        re.IGNORECASE,
    )

    _VAGUE_TIMELINES = [
        "soon",
        "shortly",
        "as soon as possible",
        "in due course",
        "at your earliest convenience",
        "in the near future",
        "whenever possible",
    ]

    _EMPTY_CTAS_RE = re.compile(
        r"\b(?:learn more|start free|get started|click here|read more|find out more)\b",
        re.IGNORECASE,
    )

    _PASSIVE_CLOSINGS = [
        "let me know",
        "feel free to reach out",
        "don't hesitate to contact",
        "do not hesitate to contact",
        "please reach out",
        "should you have any questions",
    ]

    _PITCH_VERBS_RE = re.compile(
        r"\b(?:sign up|buy now|get started|schedule|book|try|order|purchase|subscribe)\b",
        re.IGNORECASE,
    )

    _STIFF_PHRASES = ["it is", "i will", "do not", "does not", "did not", "will not", "cannot", "is not", "are not", "was not", "were not"]

    _CORPORATE_WE_RE = re.compile(r"\bwe\b", re.IGNORECASE)

    _GENERIC_APPRECIATION_RE = re.compile(
        r"\bthank you for your (?:patience|understanding|feedback|time|business|support)\b",
        re.IGNORECASE,
    )

    _SPECIFIC_TIMELINE_RE = re.compile(
        r"\b(?:by|before|on|at)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|next week|\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{1,2}\s+\w+\s*202\d)\b",
        re.IGNORECASE,
    )

    _NEXT_STEP_RE = re.compile(
        r"\b(?:i will|we will|i'll|we'll|you will|you'll)\b",
        re.IGNORECASE,
    )

    def evaluate(self, text: str) -> Dict:
        """Evaluate *text* and return a C.A.R.E. report dict."""
        c = self._evaluate_conversational(text)
        a = self._evaluate_actionable(text)
        r = self._evaluate_richer(text)
        e = self._evaluate_engaging(text)

        verdict = (
            "ready to send"
            if all([c.pass_, a.pass_, r.pass_, e.pass_])
            else "needs fixes"
        )

        return {
            "C": {"pass": c.pass_, "issues": c.issues, "fix": c.fix_lever},
            "A": {"pass": a.pass_, "issues": a.issues, "fix": a.fix_lever},
            "R": {"pass": r.pass_, "issues": r.issues, "fix": r.fix_lever},
            "E": {"pass": e.pass_, "issues": e.issues, "fix": e.fix_lever},
            "verdict": verdict,
            "original": text,
        }

    def _evaluate_conversational(self, text: str) -> PrincipleResult:
        issues: List[str] = []
        lower = text.lower()

        if self._PASSIVE_RE.search(text):
            issues.append(
                "Passive voice hides who is acting. Use 'We received...' not 'Your feedback has been received...'"
            )

        if self._CORPORATE_WE_RE.search(text) and " i " not in lower:
            issues.append(
                "Uses 'we' instead of 'I' in a direct conversation. Sounds like a brand, not a person."
            )

        if self._GENERIC_APPRECIATION_RE.search(text):
            issues.append(
                "Generic appreciation without specifics. Say what you actually did with their input."
            )

        for phrase in self._STIFF_PHRASES:
            if phrase in lower:
                issues.append(
                    "No contractions — sounds stiff. Use 'it's', 'I'll', 'don't'."
                )
                break

        fix = (
            "Replace brand language with direct ownership. Switch we→I. Add one concrete detail."
        )
        return PrincipleResult(pass_=len(issues) == 0, issues=issues, fix_lever=fix)

    def _evaluate_actionable(self, text: str) -> PrincipleResult:
        issues: List[str] = []
        lower = text.lower()

        for v in self._VAGUE_TIMELINES:
            if v in lower:
                issues.append(
                    f"Vague timeline: '{v}'. Replace with a specific date or time."
                )

        if self._EMPTY_CTAS_RE.search(text):
            issues.append(
                "CTA describes the action, not the result. 'Start free' doesn't say what happens next."
            )

        has_timeline = self._SPECIFIC_TIMELINE_RE.search(text) is not None
        has_next_step = self._NEXT_STEP_RE.search(text) is not None
        if not has_timeline and not has_next_step:
            issues.append(
                "No clear next step or timeline. State what happens next, who does it, and by when."
            )

        fix = (
            "Add timeline + next step. State what will happen, who is responsible, and when."
        )
        return PrincipleResult(pass_=len(issues) == 0, issues=issues, fix_lever=fix)

    def _evaluate_richer(self, text: str) -> PrincipleResult:
        issues: List[str] = []
        lower = text.lower()
        words = text.split()
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        has_cta = self._PITCH_VERBS_RE.search(text) is not None
        starts_with_pitch = any(
            lower.startswith(v) for v in ["sign up", "buy", "get started", "schedule", "book", "try", "order", "purchase", "subscribe"]
        )
        if has_cta and (len(sentences) <= 1 or starts_with_pitch):
            issues.append(
                "Message asks before giving. Provide useful info before any CTA."
            )

        if len(words) < 15 and "?" not in text:
            issues.append(
                "Very short response. Go one step beyond the question asked."
            )

        fix = (
            "Insert one useful insight before the CTA — name a hidden cost, explain why, or offer a next step."
        )
        return PrincipleResult(pass_=len(issues) == 0, issues=issues, fix_lever=fix)

    def _evaluate_engaging(self, text: str) -> PrincipleResult:
        issues: List[str] = []
        lower = text.lower()

        for pc in self._PASSIVE_CLOSINGS:
            if pc in lower:
                issues.append(
                    f"Passive closing: '{pc}' invites acknowledgement, not engagement. End with a decision request or specific question."
                )

        has_question = "?" in text
        has_reply_path = re.search(
            r"\b(?:reply|let me know which|choose between|decide on|confirm|pick|select)\b",
            text,
            re.IGNORECASE,
        ) is not None
        if not has_question and not has_reply_path:
            issues.append(
                "No question or clear reply path at the end. Every message must end with a reason to reply."
            )

        fix = (
            "Replace passive closing with a decision request, specific missing info, or time-bound option."
        )
        return PrincipleResult(pass_=len(issues) == 0, issues=issues, fix_lever=fix)
