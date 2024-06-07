from openai import OpenAI
from django.conf import settings

class BlogContentGenerator:
    def __init__(self, engine="text-davinci-002", max_tokens=500):
        """
        Initializes the BlogContentGenerator with specified engine and token limits.
        
        Args:
        engine (str): The OpenAI engine to use for generating content.
        max_tokens (int): The maximum number of tokens to generate.
        """
        self.engine = engine
        self.max_tokens = max_tokens
        # if not settings.OPENAI_API_KEY:
        #     raise ValueError("OPENAI_API_KEY is not set in settings.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_blog_content(self, prompt):
        """
        Generates blog content using OpenAI's GPT model based on the provided prompt.
        
        Args:
        prompt (str): The prompt to send to the GPT model for generating blog content.
        
        Returns:
        str: The generated blog content.
        """
        try:
            response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant. You will be creating a blog using specific title and content."},
                            {"role": "user", "content": prompt}
                            ])   
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to generate blog content: {str(e)}"

