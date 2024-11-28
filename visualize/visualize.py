import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import boto3
import os

# Define the set of acceptable keywords
keywords = {
"python", "developer", "api", "react", "javascript", "database", "backend",
"frontend", "fullstack", "testing", "node", "express", "html", "css", "typescript",
"cloud", "aws", "azure", "gcp", "docker", "kubernetes", "linux", "git", "version control",
"microservices", "devops", "sql", "nosql", "graphql", "web", "ui", "ux", "agile",
"scrum", "ci/cd", "automation", "machine learning", "artificial intelligence",
"data science", "data analysis", "cybersecurity", "api development", "software engineering",
"architecture", "scalability", "performance", "optimization", "architecture", "system design",
"java", "c#", "ruby", "php", "golang", "swift", "objective-c", "android", "ios", "mobile",
"flutter", "flutter", "react-native", "flutter", "testing frameworks", "unit testing", "integration testing",
"tdd", "bdd", "docker", "kubernetes", "virtualization", "cloud-native", "CI", "CD", "rest",
"web services", "big data", "etl", "spark", "hadoop", "data pipelines", "data wrangling", "api testing",
"security", "encryption", "oauth", "jwt", "authentication", "authorization"
}

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name="ca-central-1",
)

def extract_matching_keywords(file_path, keywords):
    """
    Extracts words from a .txt file that match a set of acceptable keywords and counts their frequency.

    :param file_path: Path to the .txt file.
    :param keywords: A set of acceptable keywords to match against.
    :return: A dictionary of matching keywords with their counts.
    """
    try:
        # Open and read the file
        with open(file_path, 'r') as file:
            text_content = file.read()

        # Tokenize the text into words (case insensitive, remove punctuation)
        words = text_content.lower().split()
        cleaned_words = [word.strip('.,!?()[]{}:;\'"') for word in words]

        # Find matches
        matching_keywords = [word for word in cleaned_words if word in keywords]

        # Count the occurrences of each matching keyword
        keyword_counts = dict(Counter(matching_keywords))

        return keyword_counts

    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


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
    table.put_item(Item={"id": id_key, "word_frequencies": word_frequencies})
    print(f"Stored word frequencies under id '{id_key}' in table '{table_name}'.")


def get_word_frequencies(table_name, id_key):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"id": id_key})
    if "Item" in response:
        for key, value in response["Item"]["word_frequencies"].items():
            response["Item"]["word_frequencies"][key] = int(value)
        return response["Item"].get("word_frequencies", {})
    return None


def generate_wordcloud(word_frequencies):
    """
    Generates and displays a word cloud from a dictionary of word frequencies.

    Parameters:
        word_frequencies (dict): Dictionary with words as keys and frequencies as values.
    """
    # Create a WordCloud object
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", colormap="viridis"
    )

    # Generate the word cloud using the input frequencies
    wordcloud.generate_from_frequencies(word_frequencies)

    # Plot the word cloud using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Top 10 Most Common Keywords in Job Descriptions", fontsize=16)

    output_path = "./visualize/wordcloud.png"
    print(f"Saving word cloud to {output_path}...")
    plt.savefig(output_path, format="png", dpi=300)
    plt.close()
    print("File saved successfully.")


if __name__ == "__main__":
    table_name = "TopWordFrequencies"
    id_key = "job_description_words"
    word_frequencies = {
      "python": 0, "developer": 0, "api": 0, "react": 0, "javascript": 0, "database": 0, "backend": 0, 
      "frontend": 0, "fullstack": 0, "testing": 0, "node": 0, "express": 0, "html": 0, "css": 0, "typescript": 0,
      "cloud": 0, "aws": 0, "azure": 0, "gcp": 0, "docker": 0, "kubernetes": 0, "linux": 0, "git": 0, "version control": 0, 
      "microservices": 0, "devops": 0, "sql": 0, "nosql": 0, "graphql": 0, "web": 0, "ui": 0, "ux": 0, "agile": 0, 
      "scrum": 0, "ci/cd": 0, "automation": 0, "machine learning": 0, "artificial intelligence": 0, 
      "data science": 0, "data analysis": 0, "cybersecurity": 0, "api development": 0, "software engineering": 0,
      "architecture": 0, "scalability": 0, "performance": 0, "optimization": 0, "system design": 0,
      "java": 0, "c#": 0, "ruby": 0, "php": 0, "golang": 0, "swift": 0, "objective-c": 0, "android": 0, "ios": 0, "mobile": 0, 
      "flutter": 0, "react-native": 0, "testing frameworks": 0, "unit testing": 0, "integration testing": 0, 
      "tdd": 0, "bdd": 0, "virtualization": 0, "cloud-native": 0, "CI": 0, "CD": 0, "rest": 0, 
      "web services": 0, "big data": 0, "etl": 0, "spark": 0, "hadoop": 0, "data pipelines": 0, "data wrangling": 0, "api testing": 0,
      "security": 0, "encryption": 0, "oauth": 0, "jwt": 0, "authentication": 0, "authorization": 0
    }
    store_word_frequencies(table_name, id_key, word_frequencies)

    # # Define the path to your .txt file
    # file_path = "S3/job_desc.txt"

    # # Extract matching keywords and their counts
    # keyword_counts = extract_matching_keywords(file_path, keywords)

    # # Print the keyword counts
    # if keyword_counts:
    #     print("Keyword Counts:")
    #     print(keyword_counts)
    # else:
    #     print("No matching keywords found in the file.")

    # word_frequencies = get_word_frequencies(table_name, id_key)
    # print(word_frequencies)

    # if word_frequencies:
    #     generate_wordcloud(word_frequencies)
    # else:
    #     print("No word frequencies found in DynamoDB.")
