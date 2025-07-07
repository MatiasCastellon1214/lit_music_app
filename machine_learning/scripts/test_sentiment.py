from inference import predict_sentiment

def test_predict_sentiment():
    test_texts = [
        "I love this book, it is amazing and wonderful!",
        "Terrible story, I hated every page.",
        "It was okay, not good but not bad.",
        "Absolutely fantastic, I highly recommend it!",
        "Waste of time, boring and dull."
    ]

    for text in test_texts:
        sentiment = predict_sentiment(text)
        print(f"Text: {text}")
        print(f"Predicted Sentiment: {sentiment}\n")

if __name__ == "__main__":
    test_predict_sentiment()
