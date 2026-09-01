"""Thin, testable wrapper around the real GenieX Python SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ProfileSnapshot:
    ttft_ms: float
    prompt_tokens: int
    generated_tokens: int
    prefill_tokens_per_second: float
    decode_tokens_per_second: float
    stop_reason: str

    @classmethod
    def from_sdk(cls, profile: Any) -> "ProfileSnapshot":
        return cls(
            # GenieX 0.5.0 ProfileData stores timing fields in microseconds.
            ttft_ms=float(profile.ttft) / 1_000.0,
            prompt_tokens=int(profile.prompt_tokens),
            generated_tokens=int(profile.generated_tokens),
            prefill_tokens_per_second=float(profile.prefill_speed),
            decode_tokens_per_second=float(profile.decode_speed),
            stop_reason=str(profile.stop_reason or "unknown"),
        )


@dataclass(frozen=True)
class GenerationResult:
    text: str
    profile: ProfileSnapshot


def generate_with_model(
    model: Any,
    messages: list[dict[str, str]],
    *,
    max_new_tokens: int = 256,
    temperature: float = 0.2,
    enable_thinking: bool = False,
    stream: bool = True,
    on_chunk: Callable[[str], None] | None = None,
) -> GenerationResult:
    """Format messages, generate text, and normalize GenieX profile data."""
    prompt = model.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=enable_thinking,
    )

    if stream:
        streamer = model.generate(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            stream=True,
        )
        chunks: list[str] = []
        emit = on_chunk or (lambda _chunk: None)
        for chunk in streamer:
            chunks.append(chunk)
            emit(chunk)
        if streamer.output is None:
            raise RuntimeError("GenieX stream ended without a final output profile.")
        text = streamer.output.text or "".join(chunks)
        profile = streamer.output.profile
    else:
        output = model.generate(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            stream=False,
        )
        text = output.text
        profile = output.profile

    return GenerationResult(text=text, profile=ProfileSnapshot.from_sdk(profile))


def run_geniex(
    messages: list[dict[str, str]],
    *,
    model_id: str,
    precision: str,
    device: str,
    max_new_tokens: int,
    temperature: float,
    enable_thinking: bool,
    stream: bool,
    on_chunk: Callable[[str], None] | None = None,
) -> GenerationResult:
    """Load the pinned model, generate once, and always release resources."""
    from geniex import AutoModelForCausalLM

    with AutoModelForCausalLM.from_pretrained(
        model_id,
        precision=precision,
        device_map=device,
        progress=False,
    ) as model:
        return generate_with_model(
            model,
            messages,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            enable_thinking=enable_thinking,
            stream=stream,
            on_chunk=on_chunk,
        )


def format_profile(profile: ProfileSnapshot) -> str:
    """Return a compact, readable performance summary."""
    return (
        f"TTFT: {profile.ttft_ms:.1f} ms | "
        f"Prompt: {profile.prompt_tokens} tok | "
        f"Generated: {profile.generated_tokens} tok | "
        f"Prefill: {profile.prefill_tokens_per_second:.1f} tok/s | "
        f"Decode: {profile.decode_tokens_per_second:.1f} tok/s | "
        f"Stop: {profile.stop_reason}"
    )
