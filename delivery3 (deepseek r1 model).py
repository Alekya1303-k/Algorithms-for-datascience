from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset, Features, Value, Sequence

# 1. Load the Model and Tokenizer
model_name = "deepseek-ai/deepseek-coder-1.3b-base"  # Or the specific R1 variant you want
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token # Important for training

# 2. Prepare Your Dataset

# Example:  Let's say you have a list of code strings and corresponding documentation
code_examples = [
    "def add(a, b):\n  return a + b",
    "def subtract(a, b):\n  return a - b",
    # ... more examples
]
documentation = [
    "This function adds two numbers.",
    "This function subtracts two numbers.",
    # ... more examples
]

# Combine into a single dataset suitable for language modeling
def create_dataset(code_examples, documentation, tokenizer, max_length=512):
    data = []
    for code, doc in zip(code_examples, documentation):
        # Combine code and documentation into a single string
        text = f"Code: {code}\nDocumentation: {doc}\n"  # Or any format you prefer
        tokenized = tokenizer(text, truncation=True, max_length=max_length, padding="max_length", return_tensors="np")
        data.append({
            "input_ids": tokenized["input_ids"][0],
            "attention_mask": tokenized["attention_mask"][0],
            "labels": tokenized["input_ids"][0],  # Important: Labels are the same as input_ids for LM
        })
    return Dataset.from_list(data)

dataset = create_dataset(code_examples, documentation, tokenizer)


# 3. Configure Training Arguments
training_args = TrainingArguments(
    output_dir="./deepseek-finetuned",  # Directory to save the finetuned model
    overwrite_output_dir=True,
    num_train_epochs=3,          # Adjust as needed
    per_device_train_batch_size=4, # Adjust based on your GPU memory
    save_steps=100,              # Save model checkpoints every 100 steps
    save_total_limit=2,          # Only keep the last 2 checkpoints
    learning_rate=5e-5,          # Adjust as needed
    #logging_steps=10,
    #logging_dir="./logs",
    #report_to="tensorboard",
    #fp16=True,                  # Use mixed precision training if you have a compatible GPU
)

# 4. Data Collator
# Very important for language modeling tasks!
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False) # mlm=False for CausalLM

# 5. Create Trainer and Fine-tune
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    #eval_dataset=eval_dataset,  # Optional evaluation dataset
)

trainer.train()

# 6. Save the Finetuned Model
trainer.save_model("./deepseek-finetuned")
tokenizer.save_pretrained("./deepseek-finetuned") #Save the tokenizer too

