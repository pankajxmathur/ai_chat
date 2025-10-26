import frappe
from frappe.model.document import Document
from datetime import datetime


class AIChatMessage(Document):
    """AI Chat Message model"""

    def before_insert(self):
        """Set timestamp"""
        if not self.timestamp:
            self.timestamp = datetime.now()

    def after_insert(self):
        """Update thread token count"""
        if self.tokens_used:
            thread = frappe.get_doc("AI Chat Thread", self.thread)
            thread.token_count = (thread.token_count or 0) + self.tokens_used
            thread.save(ignore_permissions=True)
