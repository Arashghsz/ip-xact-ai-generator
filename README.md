# 🧩 ip-xact-ai-generator
AI-powered system for generating valid IP-XACT components using LLMs and reinforcement learning.

## 🔍 Project Description
This project trains a fine-tuned CodeLlama-7B model to generate IP-XACT XML components based on natural language descriptions. The system incorporates:

- 🧠 Base model: Meta's CodeLlama-7b-Instruct-hf
- 🔄 Fine-tuning: LoRA adapter training on IP-XACT component examples
- 🔹 8-bit quantization for efficient inference
- ✅ GPT-3.5 Turbo for validation and assessment of generated components

The model can generate complete IP-XACT components for different interfaces (UART, Wishbone, etc.) with properly structured XML that follows IP-XACT schema requirements.

## 📊 Dataset
Our training dataset consists of paired instruction-response examples:
- **Format**: JSON structures with "instruction" and "response" fields
- **Size**: Multiple carefully crafted IP-XACT component descriptions and XML implementations
- **Examples**:
  ```json
  {
    "instruction": "Generate an IP-XACT component for a UART interface including registers for baud rate, control, status, and data.",
    "response": "<ipxact:component xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"...>...</ipxact:component>"
  }
  
  {
    "instruction": "Create an IP-XACT component for an SPI interface with master mode, supporting 4-wire configuration with clock, MOSI, MISO, and chip select signals.",
    "response": "<ipxact:component xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:ipxact=\"http://www.accellera.org/XMLSchema/IPXACT/1685-2014\"...><ipxact:vendor>example.org</ipxact:vendor><ipxact:library>spi</ipxact:library><ipxact:name>spi_master</ipxact:name>...</ipxact:component>"
  }
  ```
- **Coverage**: Various peripheral interfaces (UART, SPI, I2C, Wishbone) with different configurations and register maps

## 🛠️ Training Process
The notebook (`IP_XACT_final_version.ipynb`) implements the following training workflow:

1. **🔌 Environment Setup**:
   - Hardware: Google Colab with T4 GPU
   - Libraries: Transformers, PEFT, bitsandbytes for quantization

2. **🏗️ Model Preparation**:
   - Load CodeLlama-7b-Instruct-hf with 8-bit quantization
   - Apply LoRA adapter configuration (r=4, alpha=64, dropout=0.1)
   - Target specific attention modules (q_proj, v_proj)

3. **⚙️ Training Configuration**:
   - Epochs: 2
   - Batch size: 4 with gradient accumulation of 2
   - Learning rate: 2e-4
   - Mixed precision (fp16)
   - Optimizer: paged_adamw_32bit

4. **🔄 Tokenization and Preprocessing**:
   - Apply prompt templates
   - Token length management (up to 600 tokens)
   - Label masking for instruction-tuning

5. **🚀 Model Deployment**:
   - Push trained model to Hugging Face Hub
   - Interactive generation interface
   - Integration with GPT-3.5 validation

## ⚠️ Training Challenges
- Memory limitations requiring 8-bit quantization
- CUDA compatibility issues with certain bitsandbytes versions
- Limited dataset size requiring careful prompt engineering

# ❓ Questions to ask from mentors (Week 1-2)
- What would be the ideal output? User enter's an input and get the HW component?
- How many data do we need?
- any idea how to integrate the validation? (from CMD?)

# ❓ Questions to ask from mentors (Week 2-3)
- Can we use other verification tools? (Kaktus2 does not provide CLI or api to use.)
- The one I have developed or use LLM to verify it.
- There were multiple problems with bitsandbytes, cuda and gpu. Is it possible to use some model for training with only cpu?

# 🔍 IP-XACT Component Verification
We've implemented an AI-powered verification agent using OpenAI's GPT-3.5 Turbo to replace traditional validation tools. The agent:

1. 🔎 Analyzes generated IP-XACT components
2. ✓ Verifies XML well-formedness 
3. 📐 Checks schema compliance
4. 🔄 Validates bus interfaces
5. 🔗 Confirms port mappings
6. 📚 Verifies component references
7. 🆔 Ensures UUID uniqueness

## 📋 Usage Instructions
1. Install required packages:
   ```bash
   pip install openai
   ```

2. Set up your OpenAI API key in the environment
3. Pass your generated XML to the assessment function
4. Receive a detailed assessment report with pass/fail indicators for key validation areas

## 📝 Example Assessment Output
1. XML Well-Formed: ✅ Pass
2. Schema Compliance: ✅ Pass
3. Bus Interfaces Valid: ✅ Pass
4. Port Mappings Correct: ✅ Pass
5. Component References Exist?: ✅ Pass
