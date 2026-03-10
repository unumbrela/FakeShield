"""
Merge DTE-FDM LoRA weights into base model for inference.

After fine-tuning, DTE-FDM saves LoRA adapter files in the output directory.
This script merges them back into the base model so model_vqa.py can load it directly.
"""
import os
import sys
import argparse
import shutil

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TASK_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(PROJ_ROOT, "DTE-FDM"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lora-path", type=str,
                        default=os.path.join(TASK_DIR, "dte_fdm_finetuned"),
                        help="Path to LoRA checkpoint directory")
    parser.add_argument("--base-model", type=str,
                        default=os.path.join(PROJ_ROOT, "weight", "fakeshield-v1-22b", "DTE-FDM"),
                        help="Path to base DTE-FDM model")
    parser.add_argument("--output-dir", type=str,
                        default=os.path.join(TASK_DIR, "dte_fdm_merged"),
                        help="Output directory for merged model")
    args = parser.parse_args()

    # Find the actual checkpoint (may be in a subdirectory like checkpoint-XXX)
    lora_path = args.lora_path
    subdirs = [d for d in os.listdir(lora_path)
               if os.path.isdir(os.path.join(lora_path, d)) and d.startswith("checkpoint-")]
    if subdirs:
        # Use the latest checkpoint
        subdirs.sort(key=lambda x: int(x.split("-")[1]))
        lora_path = os.path.join(lora_path, subdirs[-1])
        print(f"Using checkpoint: {lora_path}")

    # Check for adapter files
    adapter_config = os.path.join(lora_path, "adapter_config.json")
    if not os.path.exists(adapter_config):
        print(f"ERROR: {adapter_config} not found. Check the LoRA path.")
        sys.exit(1)

    print(f"LoRA path: {lora_path}")
    print(f"Base model: {args.base_model}")
    print(f"Output dir: {args.output_dir}")

    # Use the builder to load and merge
    from llava.model.builder import load_pretrained_model

    print("\nLoading base model + LoRA weights...")
    tokenizer, model, image_processor, context_len = load_pretrained_model(
        model_path=lora_path,
        model_base=args.base_model,
        model_name="llava-v1.5-13b-lora",
        device_map="cpu",
    )

    print("Saving merged model...")
    os.makedirs(args.output_dir, exist_ok=True)
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Copy image processor config if needed
    for fname in ["preprocessor_config.json"]:
        src = os.path.join(args.base_model, fname)
        if os.path.exists(src) and not os.path.exists(os.path.join(args.output_dir, fname)):
            shutil.copy2(src, args.output_dir)

    print(f"\nMerged model saved to: {args.output_dir}")
    print(f"Use for inference: --model-path {args.output_dir}")


if __name__ == "__main__":
    main()
