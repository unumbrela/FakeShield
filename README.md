<div align="center">
<img src="./assets/Logo.png" alt="Image Alt Text" width="150" height="150">
<h3> FakeShield: Explainable Image Forgery Detection and Localization via Multi-modal Large Language Models </h3>
<!-- <h4> CVPR 2024 </h4> -->


[![arXiv](https://img.shields.io/badge/Arxiv-2410.02761-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2410.02761) 
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](https://github.com/zhipeixu/FakeShield/blob/main/LICENSE) 
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=zhipeixu.FakeShield)
[![hf_space](https://img.shields.io/badge/🤗-Huggingface%20Checkpoint-blue.svg)](https://huggingface.co/zhipeixu/fakeshield-v1-22b)
[![hf_space](https://img.shields.io/badge/🤗-MMTD%20Set%2034k-blue.svg)](https://huggingface.co/datasets/zhipeixu/MMTD-Set-34k)
[![Home Page](https://img.shields.io/badge/Project_Page-FakeShield-blue.svg)](https://zhipeixu.github.io/projects/FakeShield/)
  <br>
[![wechat](https://img.shields.io/badge/-WeChat@新智元-000000?logo=wechat&logoColor=07C160)](https://mp.weixin.qq.com/s/_ih1EycGsUTYRK15X2OrRA)
[![wechat](https://img.shields.io/badge/-WeChat@52CV-000000?logo=wechat&logoColor=07C160)](https://mp.weixin.qq.com/s/a7WpY7TuB7V3M7r3FMxRfA)
[![zhihu](https://img.shields.io/badge/-知乎-000000?logo=zhihu&logoColor=0084FF)](https://zhuanlan.zhihu.com/p/3053214498)
[![csdn](https://img.shields.io/badge/-CSDN-000000?logo=CSDN&logoColor=DC143C)](https://blog.csdn.net/amusi1994/article/details/142892876)


</div>


---


<details open><summary>💡 We also have other Copyright Protection projects that may interest you ✨. </summary><p>
<!--  may -->

> [**AvatarShield: Visual Reinforcement Learning for Human-Centric Video Forgery Detection**](https://arxiv.org/abs/2505.15173) <br>
> Zhipei Xu, Xuanyu Zhang, Xing Zhou, Jian Zhang <br>
[![github](https://img.shields.io/badge/-Github-black?logo=github)](https://github.com/zhipeixu/AvatarShield)  [![github](https://img.shields.io/github/stars/zhipeixu/AvatarShield.svg?style=social)](https://github.com/zhipeixu/AvatarShield) [![arXiv](https://img.shields.io/badge/Arxiv-2505.15173-b31b1b.svg?logo=arXiv)](https://arxiv.org/pdf/2505.15173) <br>

> [**EditGuard: Versatile Image Watermarking for Tamper Localization and Copyright Protection [CVPR 2024]**](https://arxiv.org/abs/2312.08883) <br>
> Xuanyu Zhang, Runyi Li, Jiwen Yu, Youmin Xu, Weiqi Li, Jian Zhang <br>
[![github](https://img.shields.io/badge/-Github-black?logo=github)](https://github.com/xuanyuzhang21/EditGuard)  [![github](https://img.shields.io/github/stars/xuanyuzhang21/EditGuard.svg?style=social)](https://github.com/xuanyuzhang21/EditGuard) [![arXiv](https://img.shields.io/badge/Arxiv-2312.08883-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2312.08883) <br>

> [**OmniGuard: Hybrid Manipulation Localization via Augmented Versatile Deep Image Watermarking [CVPR 2025]**](https://arxiv.org/abs/2412.01615) <br>
> Xuanyu Zhang, Zecheng Tang, Zhipei Xu, Runyi Li, Youmin Xu, Bin Chen, Feng Gao, Jian Zhang <br>
[![github](https://img.shields.io/badge/-Github-black?logo=github)](https://github.com/xuanyuzhang21/EditGuard)  [![github](https://img.shields.io/github/stars/xuanyuzhang21/OmniGuard.svg?style=social)](https://github.com/xuanyuzhang21/OmniGuard) [![arXiv](https://img.shields.io/badge/Arxiv-2412.01615-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2412.01615) <br>

</p></details>


## 📰 News
* **[2026.02.21]** 🔥🔥🔥  We have updated the **SD_Inpaint** dataset on Hugging Face, and you can access it from [here](https://huggingface.co/datasets/zhipeixu/SD_inpaint_dataset).
* **[2025.04.23]** 🤗  We have open-sourced the **MMTD-Set-34k** dataset on Hugging Face, and you can access it from [here](https://huggingface.co/datasets/zhipeixu/MMTD-Set-34k).
* **[2025.02.14]** 🤗  We ~~are progressively open-sourcing~~ have open-sourced **all code & pre-trained model weights**. Welcome to **watch** 👀 this repository for the latest updates.
* **[2025.01.23]** 🎉🎉🎉 Our FakeShield has been accepted at ICLR 2025! 
* **[2024.10.03]**  🔥 We have released **FakeShield: Explainable Image Forgery Detection and Localization via Multi-modal Large Language Models**. We present explainable IFDL tasks, constructing the MMTD-Set dataset and the FakeShield framework. Check out the [paper](https://arxiv.org/abs/2410.02761). The code and dataset are coming soon


## <img id="painting_icon" width="3%" src="https://cdn-icons-png.flaticon.com/128/1022/1022330.png"> FakeShield Overview

FakeShield is a novel multi-modal framework designed for explainable image forgery detection and localization (IFDL). Unlike traditional black-box IFDL methods, FakeShield integrates multi-modal large language models (MLLMs) to analyze manipulated images, generate tampered region masks, and provide human-understandable explanations based on pixel-level artifacts and semantic inconsistencies. To improve generalization across diverse forgery types, FakeShield introduces domain tags, which guide the model to recognize different manipulation techniques effectively. Additionally, we construct MMTD-Set, a richly annotated dataset containing multi-modal descriptions of manipulated images, fostering better interpretability. Through extensive experiments, FakeShield demonstrates superior performance in detecting and localizing various forgeries, including copy-move, splicing, removal, DeepFake, and AI-generated manipulations.

![alt text](assets/teasor.png)


## 🏆 Contributions

- **FakeShield Introduction.** We introduce FakeShield, a multi-modal framework for explainable image forgery detection and localization, which is **the first** to leverage MLLMs for the IFDL task. We also propose Domain Tag-guided Explainable Forgery Detection Module(DTE-FDM) and Multimodal Forgery Localization Module (MFLM) to improve the generalization and robustness of the models

- **Novel Explainable-IFDL Task.** We propose **the first** explainable image forgery detection and localization (e-IFDL) task, addressing the opacity of traditional IFDL methods by providing both pixel-level and semantic-level explanations.  

- **MMTD-Set Dataset Construction.** We create the MMTD-Set by enriching existing IFDL datasets using GPT-4o, generating high-quality “image-mask-description” triplets for enhanced multimodal learning.  


## 🛠️ Requirements and Installation

> **Note**: If you want to reproduce the results from our paper, please prioritize using the Docker image to set up the environment. For more details, see this [issue](https://github.com/zhipeixu/FakeShield/issues/20).

### Installation via Pip

1. Ensure your environment meets the following requirements:
    - Python == 3.9
    - Pytorch == 1.13.0
    - CUDA Version == 11.6

2. Clone the repository:
    ```bash
    git clone https://github.com/zhipeixu/FakeShield.git
    cd FakeShield
    ```
3. Install dependencies:
    ```bash
    apt update && apt install git
    pip install -r requirements.txt

    ## Install MMCV
    git clone https://github.com/open-mmlab/mmcv
    cd mmcv
    git checkout v1.4.7
    MMCV_WITH_OPS=1 pip install -e .
    ```
4. Install DTE-FDM:
    ```bash
    cd ../DTE-FDM
    pip install -e .
    pip install -e ".[train]"
    pip install flash-attn --no-build-isolation
    ```

### Installation via Docker

1. Pull the pre-built Docker image:
    ```bash
    docker pull zhipeixu/mflm:v1.0
    docker pull zhipeixu/dte-fdm:v1.0
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/zhipeixu/FakeShield.git
    cd FakeShield
    ```

3. Run the container:
    ```bash
    docker run --gpus all -it --rm \
        -v $(pwd):/workspace/FakeShield \
        zhipeixu/dte-fdm:latest /bin/bash
    
    docker run --gpus all -it --rm \
        -v $(pwd):/workspace/FakeShield \
        zhipeixu/mflm:latest /bin/bash
    ```

4. Inside the container, navigate to the repository:
    ```bash
    cd /workspace/FakeShield
    ```

5. Install MMCV:
    ```bash
    git clone https://github.com/open-mmlab/mmcv
    ```


## 🤖 Prepare Model

1. **Download FakeShield weights from Hugging Face**
   
   The model weights consist of three parts: `DTE-FDM`, `MFLM`, and `DTG`. For convenience, we have packaged them together and uploaded them to the [Hugging Face repository](https://huggingface.co/zhipeixu/fakeshield-v1-22b/tree/main).

   We recommend using `huggingface_hub` to download the weights:
   ```bash
   pip install huggingface_hub
   huggingface-cli download --resume-download zhipeixu/fakeshield-v1-22b --local-dir weight/
   ```

2. **Download pretrained SAM weight**
   
   In MFLM, we will use the SAM pre-training weights. You can use `wget` to download the `sam_vit_h_4b8939.pth` model:
   ```bash
   wget https://huggingface.co/ybelkada/segment-anything/resolve/main/checkpoints/sam_vit_h_4b8939.pth -P weight/
   ```

3. **Ensure the weights are placed correctly**
   
   Organize your `weight/` folder as follows:
   ```
    FakeShield/
    ├── weight/
    │   ├── fakeshield-v1-22b/
    │   │   ├── DTE-FDM/
    │   │   ├── MFLM/
    │   │   ├── DTG.pth
    │   ├── sam_vit_h_4b8939.pth
   ```

## 🚀 Quick Start

### CLI Demo

You can quickly run the demo script by executing:

```bash
bash scripts/cli_demo.sh
```

The `cli_demo.sh` script allows customization through the following environment variables:
- `WEIGHT_PATH`: Path to the FakeShield weight directory (default: `./weight/fakeshield-v1-22b`)
- `IMAGE_PATH`: Path to the input image (default: `./playground/image/Sp_D_CRN_A_ani0043_ani0041_0373.jpg`)
- `DTE_FDM_OUTPUT`: Path for saving the DTE-FDM output (default: `./playground/DTE-FDM_output.jsonl`)
- `MFLM_OUTPUT`: Path for saving the MFLM output (default: `./playground/DTE-FDM_output.jsonl`)

Modify these variables to suit different use cases.

## 🏋️‍♂️ Train

### Training Data Preparation

The training dataset consists of three types of data:

1. **PhotoShop Manipulation Dataset:** [CASIAv2](https://www.kaggle.com/datasets/divg07/casia-20-image-tampering-detection-dataset), [Fantastic Reality](http://zefirus.org/MAG)
2. **DeepFake Manipulation Dataset:** [FFHQ](https://cvlab.cse.msu.edu/dffd-dataset.html), [FaceAPP](https://cvlab.cse.msu.edu/dffd-dataset.html)
3. **AIGC-Editing Manipulation Dataset:** [SD_inpaint Dataset](https://huggingface.co/datasets/zhipeixu/SD_inpaint_dataset)
4. **MMTD-Set Dataset:** [MMTD-Set](https://huggingface.co/datasets/zhipeixu/MMTD-Set-34k)


### Validation Data Preparation

The validation dataset consists of three types of data:

1. **PhotoShop Manipulation Dataset:** [CASIA1+](https://github.com/proteus1991/PSCC-Net?tab=readme-ov-file#testing), [IMD2020](http://zefirus.org/MAG), [Columbia](https://www.ee.columbia.edu/ln/dvmm/downloads/authsplcuncmp/), [coverage](https://github.com/wenbihan/coverage), [NIST16](https://mfc.nist.gov/), [DSO](https://recodbr.wordpress.com/code-n-data/#dso1_dsi1), [Korus](https://pkorus.pl/downloads/dataset-realistic-tampering)
2. **DeepFake Manipulation Dataset:** [FFHQ](https://cvlab.cse.msu.edu/dffd-dataset.html), [FaceAPP](https://cvlab.cse.msu.edu/dffd-dataset.html)
3. **AIGC-Editing Manipulation Dataset:** [SD_inpaint Dataset](https://huggingface.co/datasets/zhipeixu/SD_inpaint_dataset)
4. **MMTD-Set Dataset:** [MMTD-Set](https://huggingface.co/datasets/zhipeixu/MMTD-Set-34k)

Download them from the above links and organize them as follows:

```bash
dataset/
├── photoshop/                # PhotoShop Manipulation Dataset
│   ├── CASIAv2_Tp/           # CASIAv2 Tampered Images
│   │   ├── image/
│   │   └── mask/
│   ├── CASIAv2_Au/           # CASIAv2 Authentic Images
│   │   └── image/
│   ├── FR_Tp/                # Fantastic Reality Tampered Images
│   │   ├── image/
│   │   └── mask/
│   ├── FR_Au/                # Fantastic Reality Authentic Images
│   │   └── image/
│   ├── CASIAv1+_Tp/          # CASIAv1+ Tampered Images
│   │   ├── image/
│   │   └── mask/
│   ├── CASIAv1+_Au/          # CASIAv1+ Authentic Images
│   │   └── image/
│   ├── IMD2020_Tp/           # IMD2020 Tampered Images
│   │   ├── image/
│   │   └── mask/
│   ├── IMD2020_Au/           # IMD2020 Authentic Images
│   │   └── image/
│   ├── Columbia/             # Columbia Dataset
│   │   ├── image/
│   │   └── mask/
│   ├── coverage/             # Coverage Dataset
│   │   ├── image/
│   │   └── mask/
│   ├── NIST16/               # NIST16 Dataset
│   │   ├── image/
│   │   └── mask/
│   ├── DSO/                  # DSO Dataset
│   │   ├── image/
│   │   └── mask/
│   └── Korus/                # Korus Dataset
│       ├── image/
│       └── mask/
│
├── deepfake/                 # DeepFake Manipulation Dataset
│   ├── FaceAPP_Train/        # FaceAPP Training Data
│   │   ├── image/
│   │   └── mask/
│   ├── FaceAPP_Val/          # FaceAPP Validation Data
│   │   ├── image/
│   │   └── mask/
│   ├── FFHQ_Train/           # FFHQ Training Data
│   │   └── image/
│   └── FFHQ_Val/             # FFHQ Validation Data
│       └── image/
│
├── aigc/                     # AIGC Editing Manipulation Dataset
│   ├── SD_inpaint_Train/     # Stable Diffusion Inpainting Training Data
│   │   ├── image/
│   │   └── mask/
│   ├── SD_inpaint_Val/       # Stable Diffusion Inpainting Validation Data
│   │   ├── image/
│   │   └── mask/
│   ├── COCO2017_Train/       # COCO2017 Training Data
│   │   └── image/
│   └── COCO2017_Val/         # COCO2017 Validation Data
│       └── image/
│
└── MMTD_Set/                 # Multi-Modal Tamper Description Dataset
    └── MMTD-Set-34k.json     # JSON Training File
```





### LoRA Finetune DTE-FDM

You can fine-tune DTE-FDM using LoRA with the following script:

```bash
bash ./scripts/DTE-FDM/finetune_lora.sh
```

The script allows customization through the following environment variables:
- `OUTPUT_DIR`: Directory for saving training output
- `DATA_PATH`: Path to the training dataset (JSON format)
- `WEIGHT_PATH`: Path to the pre-trained weights

Modify these variables as needed to adapt the training process to different datasets and setups.

### LoRA Finetune MFLM

You can fine-tune MFLM using LoRA with the following script:

```bash
bash ./scripts/MFLM/finetune_lora.sh
```

The script allows customization through the following environment variables:
- `OUTPUT_DIR`: Directory for saving training output
- `DATA_PATH`: Path to the training dataset
- `WEIGHT_PATH`: Path to the pre-trained weights
- `TRAIN_DATA_CHOICE`: Selecting the training dataset
- `VAL_DATA_CHOICE`: Selecting the validation dataset

Modify these variables as needed to adapt the training process to different datasets and setups.


## 🎯 Test

You can test FakeShield using the following script:

```bash
bash ./scripts/test.sh
```

The script allows customization through the following environment variables:

- `WEIGHT_PATH`: Path to the directory containing the FakeShield model weights.
- `QUESTION_PATH`: Path to the test dataset in JSONL format. This file can be generated using [`./playground/eval_jsonl.py`](https://github.com/zhipeixu/FakeShield/blob/main/playground/eval_jsonl.py).
- `DTE_FDM_OUTPUT`: Path for saving the output of the DTE-FDM model.
- `MFLM_OUTPUT`: Path for saving the output of the MFLM model.

Modify these variables as needed to adapt the evaluation process to different datasets and setups.




## 📜 Citation

```bibtex
    @inproceedings{xu2024fakeshield,
            title={FakeShield: Explainable Image Forgery Detection and Localization via Multi-modal Large Language Models},
            author={Xu, Zhipei and Zhang, Xuanyu and Li, Runyi and Tang, Zecheng and Huang, Qing and Zhang, Jian},
            booktitle={International Conference on Learning Representations},
            year={2025}
    }
```

## 🙏 Acknowledgement

We are thankful to LLaVA, groundingLMM, and LISA for releasing their models and code as open-source contributions.
