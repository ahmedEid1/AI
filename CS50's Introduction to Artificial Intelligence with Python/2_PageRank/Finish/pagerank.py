import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    states = dict()
    for pageName in corpus:
        states[pageName] = 0

    random_probability = (1 - damping_factor)/len(states)

    states[page] = random_probability

    if len(corpus[page]) != 0:
        link_probability = damping_factor / len(corpus[page])
    else:
        random_probability = 1 / len(states)

    for name in states:
        if name in corpus[page]:
            states[name] = link_probability + random_probability
        else:
            states[name] = random_probability

    return states


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []

    first_sample = random.choice(list(corpus.keys()))

    sample = first_sample
    samples.append(sample)

    for i in range(n - 1):
        model = transition_model(corpus, sample, damping_factor)
        next_sample = "".join(random.choices(list(model.keys()), weights=list(model.values()), k=1))
        samples.append(next_sample)
        sample = next_sample

    states = dict()
    for pageName in corpus:
        states[pageName] = 0

    for name in states:
        count = 0
        for item in samples:
            if item == name:
                count += 1
        states[name] = count / n

    return states


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
        # A page that has no links at all should be interpreted
    # as having one link for every page in the corpus
    for i in corpus:
        if len(corpus[i]) == 0:
            corpus[i] = set(corpus.keys())

    # after changing the  empty pages all the pages change
    # because of the new links
    new_corpus = dict()
    for i in corpus:
        new_corpus[i] = set()

    for i in corpus:
        for j in corpus[i]:
            new_corpus[j].add(i)

    pr = dict()
    for pageName in corpus:
        pr[pageName] = 1 / len(corpus)

    links = dict()
    for i in corpus:
        links[i] = len(corpus[i])

    while True:
        rank = dict()
        for name in pr:
            rank[name] = (1 - damping_factor) / len(corpus)
            for j in new_corpus[name]:
                rank[name] += damping_factor * pr[j] / links[j]

        stable = True
        for page in corpus:
            if abs(rank[page] - pr[page]) > 0.0001:
                stable = False
            pr[page] = rank[page]

        if stable:
            break

    return pr


if __name__ == "__main__":
    main()
