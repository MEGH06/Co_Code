from transformers import pipeline
import evaluate

# Load ROUGE metric
rouge = evaluate.load("rouge")
# Load the summarizer from the cache
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

# Function to summarize text and evaluate performance
def summarize(text_list):
    full_text = " ".join(text_list)
    summary = summarizer(full_text, do_sample=False)[0]["summary_text"]
    return summary
    
def evaluate_summarization(summary,reference_summaries):
    results = rouge.compute(predictions=[summary], references=reference_summaries)
    return results

# Example validation data (list of tuples with article text and reference summaries)
validation_data = [
    (["The world of artificial intelligence is rapidly advancing with new algorithms and applications."], 
     ["AI is advancing rapidly with new algorithms and applications."]),
    
    (["Machine learning is a subfield of artificial intelligence that focuses on the development of algorithms that can learn from and make predictions on data."],
     ["Machine learning focuses on creating algorithms that can learn from data and make predictions."]),
    
    (["Data science involves a mix of statistics, machine learning, and domain expertise to analyze large datasets."],
     ["Data science combines statistics, machine learning, and domain expertise to analyze data."]),
    
    (["The stock market is influenced by various factors, including global events, economic indicators, and investor sentiment."],
     ["The stock market is affected by global events, economic indicators, and investor sentiment."]),
    
    (["Quantum computing uses the principles of quantum mechanics to perform calculations that would be impossible for classical computers."],
     ["Quantum computing uses quantum mechanics to perform calculations impossible for classical computers."])
]

# Evaluate over the validation data
for text_list, reference_summary in validation_data:
    generated_summary = summarize(text_list)
    rouge_scores = evaluate_summarization(generated_summary, reference_summary)
    print(f"Generated Summary: {generated_summary}")
    print(f"ROUGE Scores: {rouge_scores}")
    print("-" * 50)


TEXT = """The rise of artificial intelligence (AI) has transformed industries across the globe, everywhere and anywhere you look. 
In every sector, AI has become a critical tool for increasing efficiency and accuracy, and it's being applied in so many ways. 
From healthcare to finance, and everywhere in between, AI has had a huge impact. 
In healthcare, AI algorithms are used to diagnose diseases, predict patient outcomes, and optimize treatment plans, and these are just a few examples of what AI can do. 
For instance, machine learning models can analyze medical images to detect conditions like cancer at an early stage, often more accurately than human doctors. 
This is extremely helpful, and it's amazing how AI can spot things that humans sometimes miss, which is a big deal, obviously.

Similarly, in the financial sector, AI is employed to detect fraudulent transactions, automate trading strategies, and improve customer service through chatbots, which are, in fact, widely used. 
Financial companies are using AI everywhere to detect fraud and provide better service. 
Companies are leveraging AI-driven analytics, which is a big deal, to make data-driven decisions, improving their competitiveness in the market. 
In fact, many companies rely on AI to make important decisions, and this reliance is growing rapidly. It's incredible how AI is revolutionizing everything.

However, the rapid adoption of AI also raises ethical and societal concerns. Issues such as data privacy, algorithmic bias, and job displacement have sparked debates about the responsible use of AI. 
Everyone's talking about it. Governments and organizations are now working to establish guidelines and regulations to ensure that AI technologies are used ethically and for the greater good. 
It's really important to make sure these technologies are used the right way, and the debate continues.

As AI continues to evolve, its potential to solve complex problems and create innovative solutions remains vast, with many more applications possible in the future. 
The challenge lies in balancing the benefits of AI with its ethical implications to build a future where technology serves humanity, which is what we all want, of course."""

print(summarize(TEXT))