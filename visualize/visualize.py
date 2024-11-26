import matplotlib.pyplot as plt
from wordcloud import WordCloud
import boto3
import os

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name='ca-central-1'
)

def store_word_frequencies(table_name, id_key, word_frequencies):
    """
    Stores a word frequency dictionary in a DynamoDB table.

    Parameters:
        table_name (str): The name of the DynamoDB table.
        id_key (str): The primary key value for the item.
        word_frequencies (dict): The dictionary to store.
    """
    table = dynamodb.Table(table_name)

    # Store the dictionary in DynamoDB as a Map
    table.put_item(
        Item={
            'id': id_key,
            'word_frequencies': word_frequencies
        }
    )
    print(f"Stored word frequencies under id '{id_key}' in table '{table_name}'.")

def get_word_frequencies(table_name, id_key):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': id_key})
    if 'Item' in response:
        return response['Item'].get('word_frequencies', {})
    return None

def generate_wordcloud(word_frequencies):
    """
    Generates and displays a word cloud from a dictionary of word frequencies.

    Parameters:
        word_frequencies (dict): Dictionary with words as keys and frequencies as values.
    """
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis")

    # Generate the word cloud using the input frequencies
    wordcloud.generate_from_frequencies(word_frequencies)

    # Plot the word cloud using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Top 10 Most Common Keywords in Job Descriptions", fontsize=16)
    plt.show()

if __name__ == "__main__":
    table_name = "TopWordFrequencies"
    id_key = "job_description_words"
    word_frequencies = {
        "flask": 2,
        "python": 400,
        "django": 50,
        "react": 30,
        "nodejs": 20,
        "sql": 100,
        "javascript": 80,
        "typescript": 25,
        "aws": 60,
        "docker": 15,
    }
    store_word_frequencies(table_name, id_key, word_frequencies)

    word_frequencies = get_word_frequencies(table_name, id_key)

    if word_frequencies:
        generate_wordcloud(word_frequencies)
    else:
        print("No word frequencies found in DynamoDB.")