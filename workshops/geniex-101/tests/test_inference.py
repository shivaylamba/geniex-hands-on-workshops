from __future__ import annotations

from types import SimpleNamespace

from solution.inference import format_profile, generate_with_model


class FakeTokenizer:
    def apply_chat_template(self, messages, **kwargs):
        assert kwargs["tokenize"] is False
        assert kwargs["add_generation_prompt"] is True
        assert kwargs["enable_thinking"] is False
        return "FORMATTED:" + messages[-1]["content"]


class FakeStreamer:
    def __init__(self):
        self.output = SimpleNamespace(
            text="hello world",
            profile=SimpleNamespace(
                ttft=12_000,
                prompt_tokens=9,
                generated_tokens=2,
                prefill_speed=100.0,
                decode_speed=20.0,
                stop_reason="eos",
            ),
        )

    def __iter__(self):
        return iter(["hello ", "world"])


class FakeModel:
    tokenizer = FakeTokenizer()

    def generate(self, prompt, **kwargs):
        assert prompt.startswith("FORMATTED:")
        assert kwargs["stream"] is True
        return FakeStreamer()


def test_streaming_generation_collects_text_and_profile() -> None:
    chunks = []
    result = generate_with_model(
        FakeModel(),
        [{"role": "user", "content": "Say hello"}],
        on_chunk=chunks.append,
    )
    assert chunks == ["hello ", "world"]
    assert result.text == "hello world"
    assert result.profile.ttft_ms == 12.0
    assert "Decode: 20.0 tok/s" in format_profile(result.profile)
