from machine_learning.scripts.inference import predict_rating

def test_predict_rating():
    test_texts = [
        "This book was amazing and kept me hooked till the end!",
        "Not a good read, I found it boring and slow.",
        "It was okay, some parts were interesting.",
        "Excellent story and well-written characters.",
        "Terrible, I regret buying this book."
    ]

    for text in test_texts:
        rating = predict_rating(text)
        print(f"Text: {text}")
        print(f"Predicted Rating: {rating}\n")

if __name__ == "__main__":
    test_predict_rating()
