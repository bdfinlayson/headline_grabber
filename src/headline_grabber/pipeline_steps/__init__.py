from transformers import AutoModelForSequenceClassification, pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer

# Load the tokenizer and model for subject classification
subject_classification_tokenizer = AutoTokenizer.from_pretrained("textattack/bert-base-uncased-ag-news")
subject_classification_model = AutoModelForSequenceClassification.from_pretrained("textattack/bert-base-uncased-ag-news")


# Load the pipeline for sentiment analysis
sentiment_analysis_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load the pre-trained Sentence-BERT model for text similarity analysis
text_similarity_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load the tokenizer and model
text_summarization_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
text_summarization_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
