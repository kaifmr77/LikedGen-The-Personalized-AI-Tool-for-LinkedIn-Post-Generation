from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, tone="Professional"):
    prompt = get_prompt(length, language, tag, tone)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, tone):
    length_str = get_length_str(length)

    prompt = f"""
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    4) Writing Tone: {tone}

    Notes:
    - If Language is Hinglish, it means a mix of Hindi and English, but script should always be English.
    - Ensure the writing matches LinkedIn's professional style while keeping the tone consistent.
    """

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\n\nUse the writing style similar to the following examples:"

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f"\n\nExample {i + 1}:\n{post_text}"
        if i == 1:  # max 2 examples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health", "Motivational"))
