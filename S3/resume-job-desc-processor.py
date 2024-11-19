import json
from collections import Counter
import boto3

def lambda_handler(event, context):
    def word_count(paragraph):
        # Remove punctuation from input paragraph and convert to lowercase
        paragraph = paragraph.lower().replace('.', '').replace(',', '')

        # Split the paragraph into a list of words
        words = paragraph.split()

        # Count the number of occurrences of each word
        word_count = Counter(words)

        # Sort the words in descending order of frequency
        sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
        print (sorted_word_count)
        return sorted_word_count

    s3 = boto3.client('s3')

    # Get bucket name and file key from the S3 event
    print(event)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Get the file object from S3
    file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)

    # Read the content of the file
    file_content = file_obj['Body'].read().decode('utf-8')

    print(f'Content of the file {file_key} from bucket {bucket_name}:')

    sorted_word_count = word_count(file_content)

    return {
        "statusCode": 200,
        "body": str(sorted_word_count)
    }
