import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestChatService(unittest.TestCase):
    """Test Chat Service"""

    def test_chat_service_initialization(self):
        """Test that ChatService can be initialized"""
        try:
            from ai_mcp_chat.services.chat_service import ChatService
            service = ChatService()
            self.assertIsNotNone(service)
            self.assertIsNotNone(service.llm_service)
        except ImportError:
            self.skipTest("ChatService not available - Frappe environment required")

    @patch('frappe.get_all')
    @patch('frappe.get_doc')
    def test_generate_response_structure(self, mock_get_doc, mock_get_all):
        """Test response generation structure"""
        try:
            from ai_mcp_chat.services.chat_service import ChatService

            # Mock thread document
            mock_thread = MagicMock()
            mock_thread.name = "test-thread"
            mock_thread.system_prompt = "Test prompt"
            mock_thread.temperature = 0.7
            mock_thread.max_tokens = 100
            mock_thread.model_used = "gpt-4"

            # Mock model config
            mock_model = MagicMock()
            mock_model.model_identifier = "gpt-4"
            mock_model.provider = "OpenAI"

            mock_get_doc.return_value = mock_model
            mock_get_all.return_value = [
                {"role": "user", "content": "Hello"}
            ]

            # Note: Actual execution would require LLM API credentials
            # This test just verifies the structure
            service = ChatService()
            self.assertTrue(hasattr(service, 'generate_response'))

        except ImportError:
            self.skipTest("ChatService not available - Frappe environment required")


if __name__ == '__main__':
    unittest.main()
