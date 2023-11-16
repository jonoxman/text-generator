from transformers import pipeline, set_seed, logging
from huggingface_hub import login
from nltk.corpus import wordnet as wn
import nltk
import re
import numpy as np

def generate_prompts(input):
    '''Given a single word or phrase topic, generate a list of prompts containing the input'''
    return [
        f"To elaborate on {input},",
        f"I first learned of {input} when",
        f"{input} has had the following impact on",
        f"Let me tell you a story about {input}. It all started",
        f"{input} has more to it than"
    ]

def generate_text(input):
    '''Generate text given a prompt. Uses gpt2'''
    generator = pipeline('text-generation', model='gpt2')
    return generator(input)[0]['generated_text']

def nouns_list(input):
    nltk.download('wordnet')
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    '''Generate a set of nouns in a given sentence'''
    regex = re.compile('[^a-zA-Z]')
    words = input.split(' ')
    result = set()
    for word in words:
        result.add(regex.sub('', word))
    return result.intersection(nouns)

def check_on_topic(input, topic):
    '''Given an input (to be generated by a model), use Facebook-BART to check whether it is likely to be about the topic.
       Likelihood is considered by taking every noun in the topic and computing the probability of that topic. 
       A definitive conclusion is considered to be reached when the probability of the topic is more than 0.2 higher than the other candidates
       Return a descriptive string saying how accurate the text was.'''
    candidate_labels = [topic]
    candidate_labels.extend([x for x in nouns_list(input)]) # check all nouns in the response
    classifier = pipeline("zero-shot-classification", mode="facebook/bart-large-mnli")
    d = classifier(input, candidate_labels)
    highest = np.argmax(d['scores']) # index of highest probability
    highest_topic = d['labels'][highest]
    second_highest = np.argsort(d['scores'])[-2]
    second_highest_topic = d['labels'][second_highest]
    result = ""
    if d['scores'][highest] > d['scores'][second_highest] + 0.2:
        if highest_topic == topic:
            result = f"'{d['sequence']}' is probably about '{topic}', with probability {d['scores'][highest]} being at least 0.2 higher than all other possibilities"
        else:
            result = f"'{d['sequence']}' is probably not about '{topic}' but rather about '{highest_topic}', with probability {d['scores'][highest]} being at least 0.2 higher than all other possibilities"
    else:
        if highest_topic == topic:
            result = f"'{d['sequence']}' is most likely about '{topic}', with probability {d['scores'][highest]}, but it may also be about '{second_highest_topic}' with probability {d['scores'][second_highest]}"
        else:
            if second_highest_topic == topic:
                result = f"'{d['sequence']}' is most likely not about '{topic}', but rather about '{highest_topic}' with probability {d['scores'][highest]}. It is however also possible it is about '{second_highest_topic}' with probability {d['scores'][second_highest]}"
            else: 
                result = f"'{d['sequence']}' is most likely not about '{topic}', but rather about '{highest_topic}' with probability {d['scores'][highest]}. The second most likely possibility is '{second_highest_topic}' with probability {d['scores'][second_highest]}"
    return result

def classify_responses(topic):
    '''Generate responses based on prompts generated from the topic. Then classify each response.'''
    prompts = generate_prompts(topic)
    responses = []
    result = []
    for p in prompts:
        responses.append(generate_text(p))
    for r in responses:
        result.append(check_on_topic(r, topic))
    return result


if __name__ == '__main__':
    #login(token='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', add_to_git_credential=True)
    logging.set_verbosity_error()
    x = input("input:")
    res = classify_responses(x)
    for r in res:
        print(r)
        print("--------------------------------")
    