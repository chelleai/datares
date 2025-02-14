import random
from lib.haiku import generate_haiku, evaluate_haiku, generate_random_topics

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
