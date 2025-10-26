import frappe
from frappe.model.document import Document


class MCPConnector(Document):
    """MCP Connector"""

    def validate(self):
        """Validate connector configuration"""
        if self.connector_type == "tcp" and not (self.host and self.port):
            frappe.throw("Host and Port are required for TCP connectors")
        elif self.connector_type == "stdio" and not self.command:
            frappe.throw("Command is required for stdio connectors")
