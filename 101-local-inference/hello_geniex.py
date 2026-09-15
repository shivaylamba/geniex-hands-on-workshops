"""Small real SDK example for Workshop 101. Run after caching the workshop model."""
import argparse
import time
from geniex import AutoModelForCausalLM


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", default="Explain on-device AI in two sentences.")
    args = parser.parse_args()
    started = time.perf_counter()
    with AutoModelForCausalLM.from_pretrained(
        "unsloth/Qwen3.5-2B-GGUF", precision="Q4_0", device_map="npu",
        n_ctx=2048, progress=False,
    ) as model:
        print(f"Load: {(time.perf_counter() - started) * 1000:.1f} ms; requested compute: npu")
        prompt = model.tokenizer.apply_chat_template(
            [{"role": "user", "content": args.question}], tokenize=False,
            add_generation_prompt=True, enable_thinking=False,
        )
        answer = model.generate(prompt, max_new_tokens=80, temperature=0.0)
        print(answer.text)
        print(f"TTFT: {answer.profile.ttft / 1000:.1f} ms (GenieX 0.5.0 units)")
        print(f"Generated tokens: {answer.profile.generated_tokens}; stop: {answer.profile.stop_reason}")


if __name__ == "__main__":
    main()
