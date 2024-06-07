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

    def generate_blog_content(self, prompt):
        """
        Generates blog content using OpenAI's GPT model based on the provided prompt.
        
        Args:
            prompt (str): The prompt to send to the GPT model for generating blog content.
        
        Returns:
            str: The generated blog content.
        """
        system_message = (
            "You are a helpful blog writing assistant."
            "You will be creating a blog using specific title," 
            "tags, and content relevant to the tags provided by the user." 
            "The user prompt will only have a list of tags. The format of your response will be:\n\n"
            "```\n"
            "Title: <title>\n"
            "Tags: <tags>\n"
            "Content: <content>\n"
            "```\n\n"
            "Note:\n"
            "* There should be no double quoted titles.\n"
            "* There should be no double quoted tags.\n"
            "* The content will also be not in a double quoted.\n"
            "* Try to include, exclude, or always do changes" 
            "in one or two tags from the list of tags provided" 
            "by the user as well as in the blog.\n"
            "* The tags should be a list of tags that are relevant" 
            "to the content of the blog post.\n"
            "* The title should be a concise and descriptive title that" 
            "captures the essence of the blog post.\n"
            "* The content should be a detailed and comprehensive content" 
            "that captures the essence of the blog post."
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ])  
            print(prompt) 
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to generate blog content: {str(e)}"

    def __str__(self):
        """
        Returns a string representation of the BlogContentGenerator settings.
        """
        return f"BlogContentGenerator(engine={self.engine}, max_tokens={self.max_tokens})"
