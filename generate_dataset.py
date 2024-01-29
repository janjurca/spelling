from lib2to3.pgen2.tokenize import tokenize
import random
from string import ascii_letters, punctuation, digits
import re
import os
from transformers import AutoTokenizer
from tqdm import tqdm
import sys


def tokenizer_check_if_text_too_long(text, tokenizer, max_length):
    data = tokenizer.batch_encode_plus([text], max_length=max_length, truncation=True, return_overflowing_tokens=True)
    if len(data["input_ids"]) > 1:
        return True
    else:
        return False  # , len(data["input_ids"][0])


def delete_characters(text, char_delete_percentage=0.01):
    modifyed_line = []
    for char in text:
        if random.random() > char_delete_percentage or char in digits:
            modifyed_line.append(char)
    return "".join(modifyed_line)


def insert_characters(text, augmentation_probability=0.008):
    modifyed_line = []
    for char in text:
        if random.random() <= augmentation_probability and char not in digits:
            modifyed_line.append(random.choice(ascii_letters+"       "))
        modifyed_line.append(char)
    return "".join(modifyed_line)


def replace_characters(text, augmentation_probability=0.01):
    modifyed_line = []
    for char in text:
        if random.random() <= augmentation_probability and char not in digits:
            modifyed_line.append(random.choice(ascii_letters+"       "))
        else:
            modifyed_line.append(char)
    return "".join(modifyed_line)


clean_chars = re.compile(r'[^A-Za-zöäüÖÄÜßàÀěĚšŠčČřŘžŽýÝáÁíÍéÉñÑôÔőŐòÒùÙúÚůŮüÜűŰľĽťŤďĎŕŔňŇ,.!?’\'$%€0-9\(\)\- ]', re.MULTILINE)


def cleanup(text):
    text = clean_chars.sub('', text)
    # print("bug: somehow all numbers are removed - this is might be due to this regex")
    # exit()
    # text = text.replace("\n", "")
    # text = text.replace('"','\\"')
    return text


clean_punctuation = re.compile(r"(?<!\d)[.,;:'?!](?!\d)")


def remove_punctuation(text):
    """Remove all punctuation from string, except if it's between digits"""
    return clean_punctuation.sub("", text)


def delete_word(text, augmentation_probability=0.001):
    if random.random() < augmentation_probability:
        words = text.split()
        if len(words) < 3:
            # do not delete word in short text, as there will be no context to guess the word
            return text
        word_to_remove = random.randint(0, len(words)-1)
        words.pop(word_to_remove)
        return " ".join(words)
    else:
        return text


if __name__ == "__main__":
    data_file = sys.argv[1]
    output_folder = sys.argv[2]
    language = os.path.basename(data_file).split(".")[0][:2]
    num_lines = sum(1 for line in open(data_file, 'r'))

    with open(data_file, 'r') as file:
        sentences = file.readlines(int(num_lines*0.5))
        sentences = [cleanup(sentence) for sentence in sentences]

    tokenizer = AutoTokenizer.from_pretrained("google/mt5-small")
    skiped_lines = 0
    processed_lines = 0
    data = []
    with open(output_folder + "/" + language+".csv", "w", encoding='utf-8') as output:
        with open(data_file, 'r') as file:
            for line in tqdm(file, total=num_lines):
                line = cleanup(line)
                if tokenizer_check_if_text_too_long(line, tokenizer, max_length=768):
                    # print(f"skipping line as its too long ({len(line)}):\n"+line)
                    skiped_lines += 1
                    continue
                if random.random() > 0.04:
                    # we will leave 2% of the data untouched, to teach the
                    # model, not to "overact" on the texts
                    new_line = delete_word(line)
                    new_line = delete_characters(new_line)
                    new_line = insert_characters(new_line)
                    new_line = replace_characters(new_line)
                    new_line = new_line.lower()
                    new_line = new_line.replace("ů", "ú")
                    new_line = remove_punctuation(new_line)
                else:
                    new_line = line
                if len(new_line) < 4 or len(new_line) > 650:
                    skiped_lines += 1
                    continue
                processed_lines += 1
                output.write(f'"{new_line.strip()}","{line.strip()}"\n')
    print(f"skipped {skiped_lines} lines and processed {processed_lines} lines")
    os.system(f"echo \"text,summary\" > {output_folder}/{language}.train.csv")
    num_lines = sum(1 for line in open(output_folder + "/" + f"{language}.csv", 'r'))
    os.system(f"head -n {num_lines-2000} {output_folder}/{language}.csv >> {output_folder}/{language}.train.csv")
    os.system(f"echo \"text,summary\" > {output_folder}/{language}.test.csv")
    os.system(f"tail -n 2000 {output_folder}/{language}.csv >> {output_folder}/{language}.test.csv")
