#Assignment 3: Taming Large Language Models
#Mariam Ahmad ID: 202202568


##Part 1: Configuration and Basic Completion

import os
from dotenv import load_dotenv
import groq

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key Loaded: {api_key}")  # Debugging line

if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Check your .env file.")

# Initialize Groq client
import groq

class LLMClient:
    def __init__(self):
        self.api_key = api_key
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama3-70b-8192"

    def complete(self, prompt, max_tokens=1000, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None


# Testing the API connection
if __name__ == "__main__":
    client = LLMClient()
    result = client.complete("Hello, how are you?")
    print(result)



##Part 2: Structured Completions 

def create_structured_prompt(text, question):
    prompt = f"""
# Analysis Report

## Input Text
{text}

## Question
{question}

## Analysis
"""
    return prompt

def extract_section(completion, section_start, section_end=None):
    start_idx = completion.find(section_start)
    if start_idx == -1:
        return None
    start_idx += len(section_start)

    if section_end is None:
        return completion[start_idx:].strip()

    end_idx = completion.find(section_end, start_idx)
    if end_idx == -1:
        return completion[start_idx:].strip()

    return completion[start_idx:end_idx].strip()



##Part 3: Classification with Confidence Analysis

def classify_with_confidence(text, categories, confidence_threshold=0.8):
    prompt = f"""
Classify the following text into one of these categories: {', '.join(categories)}.

Response format:
1. CATEGORY: [one of: {', '.join(categories)}]
2. CONFIDENCE: [high|medium|low]
3. REASONING: [explanation]

Text to classify:
{text}
"""
    response = client.complete(prompt)
    category = extract_section(response, "1. CATEGORY: ", "\n")
    confidence = extract_section(response, "2. CONFIDENCE: ", "\n")

    if confidence == "high":
        confidence_score = 0.9
    elif confidence == "medium":
        confidence_score = 0.7
    else:
        confidence_score = 0.5

    if confidence_score >= confidence_threshold:
        return {
            "category": category,
            "confidence": confidence_score,
            "reasoning": extract_section(response, "3. REASONING:")
        }
    else:
        return {"category": "uncertain", "confidence": confidence_score}



##Part 4: Prompt Strategy Comparison

def compare_prompt_strategies(texts, categories):
    strategies = {
        "basic": lambda text: f"Classify this text: {text}",
        "structured": lambda text: f"""
Classification Task
Categories: {', '.join(categories)}
Text: {text}
Classification: """,
        "few_shot": lambda text: f"""
Here are examples:

Text: "Bad service."
Classification: Negative

Text: "Great product!"
Classification: Positive

Now classify this text:
Text: "{text}"
Classification: """
    }
    results = {}
    for name, strategy in strategies.items():
        strategy_results = []
        for text in texts:
            prompt = strategy(text)
            result = client.complete(prompt)
            strategy_results.append(result)
        results[name] = strategy_results
    return results

# Example usage
texts = ["Amazing quality!", "Not worth the price."]
categories = ["Positive", "Negative", "Neutral"]
print(compare_prompt_strategies(texts, categories))



if __name__ == "__main__":
    client = LLMClient()

    # Test Basic Completion
    print("Testing Basic Completion:")
    result = client.complete("Hello, how are you?")
    print(result)

    # Test Structured Prompt
    print("\nTesting Structured Prompt:")
    prompt = create_structured_prompt("The product is great!", "What is the sentiment?")
    result = client.complete(prompt)
    print(extract_section(result, "## Analysis"))

    # Test Classification with Confidence
    print("\nTesting Classification with Confidence:")
    categories = ["Positive", "Negative", "Neutral"]
    classification_result = classify_with_confidence("The product is terrible!", categories)
    print(classification_result)

    # Test Prompt Strategy Comparison
    print("\nTesting Prompt Strategy Comparison:")
    texts = ["Amazing quality!", "Not worth the price."]
    comparison_results = compare_prompt_strategies(texts, categories)
    print(comparison_results)
