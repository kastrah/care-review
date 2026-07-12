import pytest
from care.care import CAREReview


@pytest.fixture
def review():
    return CAREReview()


class TestCAREConversational:
    """C — Conversational principle tests."""

    def test_detects_passive_voice(self, review):
        text = "Your feedback has been received and will be reviewed by the team."
        result = review.evaluate(text)
        assert result["C"]["pass"] is False
        assert any("passive voice" in issue.lower() for issue in result["C"]["issues"])

    def test_detects_corporate_we_without_i(self, review):
        text = "We have processed your request."
        result = review.evaluate(text)
        assert result["C"]["pass"] is False
        assert any("'we'" in issue for issue in result["C"]["issues"])

    def test_detects_generic_appreciation(self, review):
        text = "Thank you for your patience while we investigate."
        result = review.evaluate(text)
        assert result["C"]["pass"] is False
        assert any("generic appreciation" in issue.lower() for issue in result["C"]["issues"])

    def test_detects_no_contractions(self, review):
        text = "It is our policy to review all submissions. Do not worry."
        result = review.evaluate(text)
        assert result["C"]["pass"] is False
        assert any("contractions" in issue.lower() for issue in result["C"]["issues"])

    def test_conversational_passes_clean_text(self, review):
        text = "I got your note and I'll reply by 3pm tomorrow."
        result = review.evaluate(text)
        assert result["C"]["pass"] is True
        assert result["C"]["issues"] == []


class TestCAREActionable:
    """A — Actionable principle tests."""

    def test_flags_vague_timeline_soon(self, review):
        text = "We will get back to you soon."
        result = review.evaluate(text)
        assert result["A"]["pass"] is False
        assert any("soon" in issue for issue in result["A"]["issues"])

    def test_flags_vague_timeline_shortly(self, review):
        text = "The update will be deployed shortly."
        result = review.evaluate(text)
        assert result["A"]["pass"] is False
        assert any("shortly" in issue for issue in result["A"]["issues"])

    def test_flags_vague_timeline_asap(self, review):
        text = "I'll review this as soon as possible."
        result = review.evaluate(text)
        assert result["A"]["pass"] is False
        assert any("as soon as possible" in issue for issue in result["A"]["issues"])

    def test_flags_empty_cta(self, review):
        text = "Please get started today."
        result = review.evaluate(text)
        assert result["A"]["pass"] is False
        assert any("cta describes the action" in issue.lower() for issue in result["A"]["issues"])

    def test_fails_missing_next_step(self, review):
        text = "I am happy to assist you."
        result = review.evaluate(text)
        assert result["A"]["pass"] is False
        assert any("no clear next step" in issue.lower() for issue in result["A"]["issues"])

    def test_actionable_passes_with_timeline(self, review):
        text = "I will fix the bug by Friday."
        result = review.evaluate(text)
        assert result["A"]["pass"] is True
        assert result["A"]["issues"] == []


class TestCARERicherThanAsked:
    """R — Richer than Asked principle tests."""

    def test_flags_pure_pitch(self, review):
        text = "Sign up now for our awesome service!"
        result = review.evaluate(text)
        assert result["R"]["pass"] is False
        assert any("message asks before giving" in issue.lower() for issue in result["R"]["issues"])

    def test_flags_minimal_answer(self, review):
        text = "No, that is not possible."
        result = review.evaluate(text)
        assert result["R"]["pass"] is False
        assert any("very short response" in issue.lower() for issue in result["R"]["issues"])

    def test_richer_passes_with_insight(self, review):
        text = (
            "No, we don't support custom export sizes directly. However, you can export "
            "to SVG first and then scale it in any vector tool without losing quality. "
            "I can walk you through this process if you'd like?"
        )
        result = review.evaluate(text)
        assert result["R"]["pass"] is True
        assert result["R"]["issues"] == []


class TestCAREEngagingDialogue:
    """E — Engaging Dialogue principle tests."""

    def test_fails_passive_closing_let_me_know(self, review):
        text = "Let me know what you think."
        result = review.evaluate(text)
        assert result["E"]["pass"] is False
        assert any("passive closing" in issue.lower() for issue in result["E"]["issues"])

    def test_fails_passive_closing_feel_free(self, review):
        text = "Feel free to reach out if you have questions."
        result = review.evaluate(text)
        assert result["E"]["pass"] is False
        assert any("passive closing" in issue.lower() for issue in result["E"]["issues"])

    def test_fails_missing_reply_path(self, review):
        text = "The package is on the way."
        result = review.evaluate(text)
        assert result["E"]["pass"] is False
        assert any("no question or clear reply path" in issue.lower() for issue in result["E"]["issues"])

    def test_engaging_passes_with_question(self, review):
        text = "Which of these delivery times works best for you?"
        result = review.evaluate(text)
        assert result["E"]["pass"] is True
        assert result["E"]["issues"] == []


class TestCAREFullEvaluate:
    """Overall CAREReview integration tests."""

    def test_returns_correct_structure(self, review):
        text = "Hello world"
        result = review.evaluate(text)
        assert "C" in result
        assert "A" in result
        assert "R" in result
        assert "E" in result
        assert "verdict" in result
        assert "original" in result

    def test_verdict_ready_when_all_pass(self, review):
        text = (
            "I checked the issue and I'll deploy the fix by Friday afternoon. "
            "This fixes the SVG export sizing bug. "
            "Which of these delivery times works best for you?"
        )
        result = review.evaluate(text)
        assert result["verdict"] == "ready to send"

    def test_verdict_needs_fixes_when_any_fail(self, review):
        text = "Your feedback has been received."
        result = review.evaluate(text)
        assert result["verdict"] == "needs fixes"

    def test_evaluate_preserves_original(self, review):
        text = "Original raw string."
        result = review.evaluate(text)
        assert result["original"] == text

    def test_fixture_message_sample(self, review):
        import pathlib
        fixture = pathlib.Path(__file__).with_name("fixtures") / "message_sample.txt"
        text = fixture.read_text(encoding="utf-8")
        result = review.evaluate(text)

        assert result["C"]["pass"] is False
        assert result["A"]["pass"] is False
        assert result["E"]["pass"] is False
        assert result["verdict"] == "needs fixes"
