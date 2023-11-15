from transformers import pipeline, set_seed
from huggingface_hub import login

def generate_prompt(input):
    return None

def generate_text(input):
    '''Generate text given a prompt. Uses gpt22'''
    generator = pipeline('text-generation', model='gpt2')
    return generator(input)[0]['generated_text']

if __name__ == '__main__':
    #login(token='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', add_to_git_credential=True)
    x = input("input:")
    print(generate_text(x))
