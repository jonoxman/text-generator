from text_generation import generate_prompts, generate_text, check_on_topic

def generate_and_classify(topic, prompts):
    """
    Generate responses based on prompts generated from the topic. Then classify each response.
    
    Args:
        topic (str): The expected topic to check for.
        prompts (list): A list of prompts to generate responses from.
    """
    responses = []
    result = []
    for p in prompts:
        responses.append(generate_text(p))
    for r in responses:
        result.append(check_on_topic(r, topic))
    return result

if __name__ == '__main__':
    #logging.set_verbosity_error()
    x = input("input:")
    res = generate_and_classify(x, generate_prompts(x))
    for r in res:
        print(r)
        print("--------------------------------")
    