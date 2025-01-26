from transformers import pipeline

def summarize_content(text_list):
    full_text = " ".join(text_list)
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
    summary = summarizer(full_text, do_sample=False)[0]["summary_text"]
    return summary
