from openai import OpenAI
import random  # Add this import at the top
client = OpenAI()

def generate_haiku(subject):
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "user", "content": f"write a haiku about {subject}"}
        ]
    )

    return completion.choices[0].message.content

def evaluate_haiku(subject, haiku):
    evaluate_haiku = f"""
    You are a haiku evaluator. You will be given a haiku and you will need to evaluate it.

Haiku: {haiku}

Can you confirm yes or no if the haiku is about {subject}? PLEASE ONLY RESPOND WITH YES OR NO.
"""

    print("Evaluating haiku...")

    completion = client.chat.completions.create(
        model="gpt-4",
        store=True,
        messages=[
            {"role": "user", "content": evaluate_haiku}
        ]
    )

    print("Evaluated haiku...")
    return completion.choices[0].message.content

def generate_random_topics(num_topics=5):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Generate {num_topics} random, interesting topics for haikus. Respond with ONLY the topics, one per line, no numbers or bullets."}
        ]
    )
    
    topics = completion.choices[0].message.content.strip().split('\n')
    return topics

# Example usage
if __name__ == "__main__":
    # Generate random topics and select one
    topics = generate_random_topics()
    subject = random.choice(topics)
    print("Available topics:", topics)
    print(f"Selected topic: {subject}")
    
    haiku = generate_haiku(subject)
    print(f"\nGenerated haiku about {subject}:")
    print(haiku)
    
    result = evaluate_haiku(subject, haiku)
    print(f"Is the haiku about {subject}? {result}")