"""
Convert MFLM DeepSpeed checkpoint to HuggingFace-compatible format for inference.

After MFLM fine-tuning, the checkpoint is saved by DeepSpeed in:
  output/mflm_finetuned/ckpt_model_best/

This script:
1. Loads the DeepSpeed ZeRO-2 checkpoint
2. Merges LoRA weights into the base model
3. Saves in HuggingFace format that test.py can load via from_pretrained()
"""
import os
import sys
import glob
import json
import torch
import argparse
from collections import OrderedDict

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TASK_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(PROJ_ROOT, "MFLM"))


def find_checkpoint_dir(base_dir):
    """Find the best checkpoint directory."""
    best_dir = os.path.join(base_dir, "ckpt_model_best")
    if os.path.exists(best_dir):
        return best_dir
    # Fallback to last epoch
    last_dir = os.path.join(base_dir, "ckpt_model_last_epoch")
    if os.path.exists(last_dir):
        return last_dir
    # Search in output/ subdirectory
    output_best = os.path.join("output", base_dir, "ckpt_model_best")
    if os.path.exists(output_best):
        return output_best
    raise FileNotFoundError(f"No checkpoint found in {base_dir}")


def convert_zero2_checkpoint(ckpt_dir):
    """
    Convert DeepSpeed ZeRO-2 checkpoint to a single state_dict.
    ZeRO-2 stores the full model params (not partitioned like ZeRO-3),
    so we just need to load mp_rank_00_model_states.pt.
    """
    # Find the global_step directory
    latest_file = os.path.join(ckpt_dir, "latest")
    if os.path.exists(latest_file):
        with open(latest_file) as f:
            step_dir = f.read().strip()
        model_file = os.path.join(ckpt_dir, step_dir, "mp_rank_00_model_states.pt")
    else:
        # Try to find model states directly
        model_files = glob.glob(os.path.join(ckpt_dir, "*/mp_rank_00_model_states.pt"))
        if not model_files:
            raise FileNotFoundError(f"No model_states.pt found in {ckpt_dir}")
        model_file = model_files[0]

    print(f"Loading checkpoint from: {model_file}")
    state = torch.load(model_file, map_location="cpu", weights_only=False)

    # DeepSpeed wraps the state dict under 'module' key
    if "module" in state:
        state_dict = state["module"]
    else:
        state_dict = state

    return state_dict


def merge_lora_state_dict(state_dict):
    """
    Merge LoRA weights (lora_A, lora_B) into the base weights.
    LoRA formula: W_merged = W_base + (B @ A) * scaling
    """
    # Find all LoRA parameter pairs
    lora_keys = [k for k in state_dict if "lora_A" in k or "lora_B" in k]
    if not lora_keys:
        print("No LoRA weights found, returning state_dict as-is")
        return state_dict

    # Group by base parameter name
    lora_pairs = {}
    for k in lora_keys:
        # Key patterns: base.model.layers.X.self_attn.q_proj.lora_A.default.weight
        if "lora_A" in k:
            base_key = k.replace(".lora_A.default.weight", ".weight")
            if base_key not in lora_pairs:
                lora_pairs[base_key] = {}
            lora_pairs[base_key]["A"] = k
        elif "lora_B" in k:
            base_key = k.replace(".lora_B.default.weight", ".weight")
            if base_key not in lora_pairs:
                lora_pairs[base_key] = {}
            lora_pairs[base_key]["B"] = k

    # Try to get LoRA scaling from config
    # Default: scaling = lora_alpha / lora_r
    # From the training script: lora_r=8, lora_alpha=16 -> scaling=2.0
    scaling = 16.0 / 8.0  # lora_alpha / lora_r

    merged_count = 0
    new_state_dict = OrderedDict()

    for k, v in state_dict.items():
        if "lora_A" in k or "lora_B" in k:
            continue  # Skip LoRA params, will be merged
        new_state_dict[k] = v

    for base_key, pair in lora_pairs.items():
        if "A" in pair and "B" in pair:
            lora_A = state_dict[pair["A"]]  # (r, in_features)
            lora_B = state_dict[pair["B"]]  # (out_features, r)
            delta = (lora_B @ lora_A) * scaling

            # The base key might have 'base_model.model.' prefix from PEFT
            # Find the actual key in state_dict
            actual_base_key = base_key
            if actual_base_key not in new_state_dict:
                # Try with base_model.model prefix
                alt_key = "base_model.model." + base_key
                if alt_key in new_state_dict:
                    actual_base_key = alt_key
                else:
                    print(f"WARNING: base key {base_key} not found, skipping merge")
                    continue

            new_state_dict[actual_base_key] = new_state_dict[actual_base_key] + delta
            merged_count += 1

    print(f"Merged {merged_count} LoRA pairs (scaling={scaling})")

    # Remove PEFT wrapper prefixes: base_model.model.X -> X
    final_dict = OrderedDict()
    for k, v in new_state_dict.items():
        new_k = k.replace("base_model.model.", "")
        final_dict[new_k] = v

    return final_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt-dir", type=str,
                        default=os.path.join(TASK_DIR, "mflm_finetuned"),
                        help="Directory containing the DeepSpeed checkpoint")
    parser.add_argument("--base-model", type=str,
                        default=os.path.join(PROJ_ROOT, "weight", "fakeshield-v1-22b", "MFLM"),
                        help="Base MFLM model directory (for config files)")
    parser.add_argument("--output-dir", type=str,
                        default=os.path.join(TASK_DIR, "mflm_merged"),
                        help="Output directory for merged model")
    args = parser.parse_args()

    # Find checkpoint
    ckpt_dir = find_checkpoint_dir(args.ckpt_dir)
    print(f"Checkpoint dir: {ckpt_dir}")

    # Load and convert
    state_dict = convert_zero2_checkpoint(ckpt_dir)
    merged_dict = merge_lora_state_dict(state_dict)

    # Save merged weights
    os.makedirs(args.output_dir, exist_ok=True)

    # Copy config files from base model
    import shutil
    for config_file in ["config.json", "generation_config.json",
                        "special_tokens_map.json", "tokenizer.model",
                        "tokenizer_config.json"]:
        src = os.path.join(args.base_model, config_file)
        if os.path.exists(src):
            shutil.copy2(src, args.output_dir)
            print(f"Copied {config_file}")

    # Save merged weights
    # Split into shards if too large
    total_size = sum(v.numel() * v.element_size() for v in merged_dict.values())
    print(f"Total model size: {total_size / 1e9:.2f} GB")

    if total_size > 5e9:  # > 5GB, save in shards
        shard_size = 4 * 1024 * 1024 * 1024  # 4GB per shard
        current_shard = OrderedDict()
        current_size = 0
        shard_idx = 1
        index = {"weight_map": {}, "metadata": {"total_size": total_size}}

        for k, v in merged_dict.items():
            param_size = v.numel() * v.element_size()
            if current_size + param_size > shard_size and current_shard:
                shard_name = f"pytorch_model-{shard_idx:05d}-of-XXXXX.bin"
                torch.save(current_shard, os.path.join(args.output_dir, shard_name))
                print(f"Saved shard {shard_idx}: {len(current_shard)} params")
                shard_idx += 1
                current_shard = OrderedDict()
                current_size = 0
            current_shard[k] = v
            current_size += param_size

        if current_shard:
            shard_name = f"pytorch_model-{shard_idx:05d}-of-XXXXX.bin"
            torch.save(current_shard, os.path.join(args.output_dir, shard_name))
            print(f"Saved shard {shard_idx}: {len(current_shard)} params")

        # Fix shard names
        total_shards = shard_idx
        for i in range(1, total_shards + 1):
            old_name = f"pytorch_model-{i:05d}-of-XXXXX.bin"
            new_name = f"pytorch_model-{i:05d}-of-{total_shards:05d}.bin"
            os.rename(
                os.path.join(args.output_dir, old_name),
                os.path.join(args.output_dir, new_name)
            )
            # Update index
            for k in merged_dict:
                pass  # will rebuild

        # Rebuild index
        shard_idx = 1
        current_size = 0
        for k, v in merged_dict.items():
            param_size = v.numel() * v.element_size()
            if current_size + param_size > shard_size and current_size > 0:
                shard_idx += 1
                current_size = 0
            shard_name = f"pytorch_model-{shard_idx:05d}-of-{total_shards:05d}.bin"
            index["weight_map"][k] = shard_name
            current_size += param_size

        with open(os.path.join(args.output_dir, "pytorch_model.bin.index.json"), "w") as f:
            json.dump(index, f, indent=2)
    else:
        torch.save(merged_dict, os.path.join(args.output_dir, "pytorch_model.bin"))

    print(f"\nMerged model saved to: {args.output_dir}")
    print(f"Use for inference: --version {args.output_dir}")


if __name__ == "__main__":
    main()
