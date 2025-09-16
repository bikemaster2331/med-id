from datasets import load_dataset
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
import numpy as np
import evaluate

# 1. Load your dataset
dataset = load_dataset('csv', data_files={'train': 'data.csv', 'test': 'data.csv'})  # you can split into train/test separately

# 2. Tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

def tokenize(batch):
    return tokenizer(batch['text'], padding=True, truncation=True)

dataset = dataset.map(tokenize, batched=True)

# 3. Encode labels
label2id = {"OTHER": 0, "MED_NAME": 1}
id2label = {0: "OTHER", 1: "MED_NAME"}
dataset = dataset.map(lambda x: {"labels": [label2id[l] for l in x["label"]]})

# 4. Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
    id2label=id2label,
    label2id=label2id
)

# 5. Training setup
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return accuracy.compute(predictions=preds, references=labels)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 6. Train 🚀
trainer.train()

# 7. Save model
trainer.save_model("./med_classifier_transformer")
tokenizer.save_pretrained("./med_classifier_transformer")
