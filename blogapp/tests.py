
# Create your tests here.
from django.test import TestCase, Client
from unittest.mock import patch
from django.core.mail import EmailMessage
from celery.result import AsyncResult
from blogapp.tasks import send_mail_celery_func  # Replace with your actual task location      
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger("custom_logger")
class SendMailTest(TestCase):
    
    @patch('django.core.mail.EmailMessage.send')  # Mock EmailMessage.send to prevent real sending
    def test_email_is_sent(self, mock_send):
        """Test that the email send method is called."""
        
        email = EmailMessage(
            subject="Test Subject",
            body="Test Body",
            from_email="test@example.com",
            to=["testreceiver@example.com"]
        )
        
        email.send()
        
        mock_send.assert_called_once()  # Verify send() was called once
        with self.assertLogs("custom_logger", level="INFO") as log:
            logger.info("Test email sent successfully.")
        
        self.assertIn("Test email sent successfully.", log.output[0])  # Verify log message