import frappe
from ai_mcp_chat.services.llm_service import LLMService


class ChatService:
    """Core chat operations"""

    def __init__(self):
        self.llm_service = LLMService()

    def generate_response(self, thread_doc):
        """Generate AI response"""
        try:
            # Get messages
            messages = frappe.get_all(
                "AI Chat Message",
                filters={"thread": thread_doc.name},
                fields=["role", "content"],
                order_by="timestamp asc"
            )

            # Get model config
            model_config = frappe.get_doc(
                "LLM Model Configuration",
                thread_doc.model_used
            )

            # Format messages
            formatted_msgs = [
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ]

            # Stream response
            accumulated = ""
            for chunk in self.llm_service.stream_completion(
                model=model_config.model_identifier,
                messages=formatted_msgs,
                system_prompt=thread_doc.system_prompt,
                temperature=thread_doc.temperature,
                max_tokens=thread_doc.max_tokens,
                provider=model_config.provider
            ):
                accumulated += chunk.get("content", "")

            # Save assistant message
            response_msg = frappe.get_doc({
                "doctype": "AI Chat Message",
                "thread": thread_doc.name,
                "role": "assistant",
                "content": accumulated,
                "model_used": model_config.model_identifier
            })
            response_msg.insert()
            frappe.db.commit()

            return {
                "success": True,
                "content": accumulated,
                "message_id": response_msg.name
            }
        except Exception as e:
            frappe.log_error(str(e), "Generate Response")
            raise
