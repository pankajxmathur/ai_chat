import frappe
import os
from typing import Generator, List, Dict


class LLMService:
    """Multi-provider LLM service"""

    def stream_completion(self, model: str, messages: List[Dict],
                         system_prompt: str, temperature: float,
                         max_tokens: int, provider: str) -> Generator:
        """Stream LLM completion"""

        if provider == "OpenAI":
            yield from self._openai_stream(
                model, messages, system_prompt, temperature, max_tokens
            )
        elif provider == "Anthropic":
            yield from self._anthropic_stream(
                model, messages, system_prompt, temperature, max_tokens
            )
        elif provider == "Google":
            yield from self._google_stream(
                model, messages, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _openai_stream(self, model: str, messages: List[Dict],
                      system_prompt: str, temperature: float,
                      max_tokens: int) -> Generator:
        """OpenAI streaming"""
        try:
            import openai

            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in environment")

            client = openai.OpenAI(api_key=api_key)

            system_msg = {"role": "system", "content": system_prompt}
            all_msgs = [system_msg] + messages if system_prompt else messages

            stream = client.chat.completions.create(
                model=model,
                messages=all_msgs,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield {
                        "content": chunk.choices[0].delta.content,
                        "tokens": 0
                    }
        except Exception as e:
            frappe.log_error(str(e), "OpenAI Stream")
            raise

    def _anthropic_stream(self, model: str, messages: List[Dict],
                         system_prompt: str, temperature: float,
                         max_tokens: int) -> Generator:
        """Anthropic Claude streaming"""
        try:
            import anthropic

            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set in environment")

            client = anthropic.Anthropic(api_key=api_key)

            with client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt or "",
                messages=messages,
                temperature=temperature
            ) as stream:
                for text in stream.text_stream:
                    yield {
                        "content": text,
                        "tokens": 0
                    }
        except Exception as e:
            frappe.log_error(str(e), "Anthropic Stream")
            raise

    def _google_stream(self, model: str, messages: List[Dict],
                      system_prompt: str, temperature: float,
                      max_tokens: int) -> Generator:
        """Google Gemini streaming"""
        try:
            import google.generativeai as genai

            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not set in environment")

            genai.configure(api_key=api_key)

            # Convert messages to Gemini format
            prompt_parts = []
            if system_prompt:
                prompt_parts.append(system_prompt)

            for msg in messages:
                role_prefix = "User: " if msg["role"] == "user" else "Assistant: "
                prompt_parts.append(f"{role_prefix}{msg['content']}")

            prompt = "\n\n".join(prompt_parts)

            model_obj = genai.GenerativeModel(model_name=model)
            response = model_obj.generate_content(
                prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )

            for chunk in response:
                if chunk.text:
                    yield {
                        "content": chunk.text,
                        "tokens": 0
                    }
        except Exception as e:
            frappe.log_error(str(e), "Google Stream")
            raise
