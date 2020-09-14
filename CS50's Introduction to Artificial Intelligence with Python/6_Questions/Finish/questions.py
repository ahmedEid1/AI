import math
import os
import string
import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files_dict = dict()

    with os.scandir(directory) as files:
        for file in files:
            with open(os.path.join(file.path), encoding="utf8") as f:
                data = f.read()
                files_dict[file.name] = data
    return files_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()

    words = nltk.word_tokenize(document)

    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")

    for word in words:
        if word in punctuation or word in stopwords:
            words.remove(word)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()

    for k in documents:
        for w in documents[k]:
            words.add(w)

    total = len(documents)

    idfs = dict()

    for word in words:
        count = 0
        for k in documents:
            if word in documents[k]:
                count += 1
        idfs[word] = math.log(total / count)

    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranks = dict()
    for file in files.keys():
        ranks[file] = 0

    for file in files.keys():
        for word in query:
            for w in files[file]:
                count = 0
                if word == w:
                    count += 1
                tf = count
                ranks[file] += (tf * idfs[w])

    ranked_files = [k for k, v in sorted(ranks.items(), key=lambda item: item[1])]
    ranked_files.reverse()
    return ranked_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = dict()
    qtd = dict()
    for sentence in sentences.keys():
        ranks[sentence] = 0

    for sentence in sentences.keys():
        count = 0
        for word in query:
            if word in sentences[sentence]:
                count += 1
                ranks[sentence] += idfs[word]
        qtd[sentence] = count / len(sentences[sentence])

    sents = []
    for k in ranks.keys():
        sents.append(k)

    sents.sort(key=lambda x: (ranks[x], qtd[x]), reverse=True)

    return sents[:n]







if __name__ == "__main__":
    main()
