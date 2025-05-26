import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Tuple, Dict
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI client with the correct environment variable name and no additional options
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Assistant ID for story generation
STORY_ASSISTANT_ID = "asst_lgs9l7lRtH77ThjUx9BzRSTX"

def generate_story(prompt: str = "Create a short story") -> Tuple[str, List[str]]:
    """
    Generate a story using a specific OpenAI Assistant.
    
    Args:
        prompt: The prompt to guide story generation
        
    Returns:
        Tuple containing the title and list of sentences (including title as first sentence)
    """
    try:
        # Create a thread
        thread = client.beta.threads.create()

        # Add a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=STORY_ASSISTANT_ID
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status in ['failed', 'cancelled', 'expired']:
                raise Exception(f"Assistant run failed with status: {run_status.status}")
            time.sleep(1)  # Wait for 1 second before checking again

        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        
        # Get the latest assistant message
        assistant_message = next((msg for msg in messages if msg.role == "assistant"), None)
        if not assistant_message:
            raise Exception("No response from assistant")

        # Extract the story text
        story_text = assistant_message.content[0].text.value.strip()
        
        # Split into sentences
        sentences = []
        for line in story_text.split('\n'):
            line = line.strip()
            if line:
                # Split by periods and add each sentence
                for sentence in line.split('.'):
                    if sentence.strip():
                        sentences.append(sentence.strip())
        
        # Ensure we have exactly 7 sentences
        if len(sentences) < 7:
            raise Exception(f"Assistant generated only {len(sentences)} sentences, expected 7")
        
        # First sentence is the title, rest is the story
        title = sentences[0]
        return title, sentences[:7]  # Return all 7 sentences (title + 6 story sentences)
        
    except Exception as e:
        print(f"Error generating story: {e}")
        return "Error generating story", ["Error"] * 7

def generate_additional_sentences(count: int, context: str) -> List[str]:
    """This function is no longer used as we're using the assistant for story generation"""
    return ["Error generating sentence"] * count

def generate_image(prompt: str) -> str:
    """
    Generate an image using DALL-E for a given prompt
    
    Args:
        prompt: The text description to generate an image for
        
    Returns:
        URL of the generated image
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Create a comic panel illustration for: {prompt}",
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return ""

async def generate_comic_panels(sentences: List[str]) -> List[Dict[str, str]]:
    """
    Generate comic panels with images for each sentence
    
    Args:
        sentences: List of sentences to generate images for
        
    Returns:
        List of dictionaries containing sentence and image_url for each panel
    """
    panels = []
    for i, sentence in enumerate(sentences):
        # Generate image for the sentence
        image_url = generate_image(sentence)
        
        # Create panel data
        panel = {
            "sentence": sentence,
            "image_url": image_url,
            "panel_order": i + 1
        }
        panels.append(panel)
    
    return panels 