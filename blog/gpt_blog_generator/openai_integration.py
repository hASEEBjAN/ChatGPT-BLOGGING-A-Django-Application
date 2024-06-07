"""
Module to integrate OpenAI's GPT models for generating blog content within a Django application.
"""
import os
from openai import OpenAI
from django.conf import settings

class BlogContentGenerator:
    """
    A class to generate blog content using OpenAI's GPT models.
    """
    def __init__(self, engine="text-davinci-002", max_tokens=500):
        """
        Initializes the BlogContentGenerator with specified engine and token limits.
        
        Args:
            engine (str): The OpenAI engine to use for generating content.
            max_tokens (int): The maximum number of tokens to generate.
        """
        self.engine = engine
        self.max_tokens = max_tokens
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in settings.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def load_system_message(self, file_path):
        """
        Loads the system message from a text file.
        
        Args:
            file_path (str): The path to the text file containing the system message.
        
        Returns:
            str: The content of the system message.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def generate_blog_content(self, prompt):
        """
        Generates blog content using OpenAI's GPT model based on the provided prompt.
        
        Args:
            prompt (str): The prompt to send to the GPT model for generating blog content.
        
        Returns:
            str: The generated blog content.
        """
        system_message = self.load_system_message('blog/gpt_blog_generator/system_message.txt')
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ])
            print(prompt)
            return response.choices[0].message.content
        except Exception as specific_error:
            return f"Failed to generate blog content: {str(specific_error)}"

    def __str__(self):
        """
        Returns a string representation of the BlogContentGenerator settings.
        """
        return f"BlogContentGenerator(engine={self.engine}, max_tokens={self.max_tokens})"
