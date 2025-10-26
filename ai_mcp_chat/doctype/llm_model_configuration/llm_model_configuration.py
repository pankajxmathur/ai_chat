import frappe
from frappe.model.document import Document


class LLMModelConfiguration(Document):
    """LLM Model Configuration"""

    def validate(self):
        """Validate model configuration"""
        if self.provider in ["OpenAI", "Anthropic", "Google"] and not self.api_key_field:
            frappe.throw("API Key Field Name is required for this provider")
