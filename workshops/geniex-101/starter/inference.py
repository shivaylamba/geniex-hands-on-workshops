"""Working GenieX inference path used by the starter application."""

from __future__ import annotations

from typing import Callable


def run_geniex(
    messages: list[dict[str, str]],
    *,
    model_id: str,
    precision: str = "Q4_0",
    device: str = "npu",
    max_new_tokens: int = 256,
    on_chunk: Callable[[str], None] | None = None,
):
    from geniex import AutoModelForCausalLM

    with AutoModelForCausalLM.from_pretrained(
        model_id,
        precision=precision,
        device_map=device,
        progress=False,
    ) as model:
        prompt = model.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        streamer = model.generate(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=0.2,
            stream=True,
        )
        chunks = []
        for chunk in streamer:
            chunks.append(chunk)
            if on_chunk:
                on_chunk(chunk)
        if streamer.output is None:
            raise RuntimeError("GenieX stream ended without a result.")
        return "".join(chunks), streamer.output.profile
