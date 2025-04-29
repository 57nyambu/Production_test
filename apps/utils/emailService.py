import resend
from Root.settings.base import RESEND_KEY

resend.api_key = RESEND_KEY


def welcomeEmail(user):
    params: resend.Emails.SendParams = {
        "from": "Finarchitect <welcome@finarchitect.site>",
        "to": [f"{user['email']}"],
        "subject": "Welcome to FinArchitect!",
        "html": f"""
        <html>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f9f9f9;">
            <table width="100%" style="border-collapse: collapse; background-color: #f9f9f9;">
                <tr>
                    <td align="center">
                        <table width="600px" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15); margin: 20px 0;">
                            <tr>
                                <td style="background-color: #0078d4; color: #ffffff; padding: 20px; text-align: center;">
                                    <h1 style="margin: 0; font-size: 24px;">Welcome to Finarchitect!</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 20px; color: #333;">
                                    <p style="font-size: 16px;">Dear {user['first_name']},</p>
                                    <p style="font-size: 16px; line-height: 1.5;">
                                        We are thrilled to have you with us. Thank you for signing up and becoming a part of the Finarchitect community!
                                    </p>
                                    <p style="font-size: 16px; line-height: 1.5;">
                                        At Finarchitect, we strive to provide you with the best financial architecture solutions tailored to your needs.
                                    </p>
                                    <p style="font-size: 16px; line-height: 1.5;">Here are some next steps to get you started:</p>
                                    <ul style="font-size: 16px; line-height: 1.5; padding-left: 20px;">
                                        <li>Explore your dashboard and familiarize yourself with the features.</li>
                                        <li>Connect your accounts and start managing your finances efficiently.</li>
                                        <li>Check out our resource center for tips and best practices.</li>
                                    </ul>
                                    <p style="font-size: 16px; line-height: 1.5;">
                                        If you have any questions or need assistance, feel free to reach out to our support team at 
                                        <a href="mailto:support@finarchitect.site" style="color: #0078d4; text-decoration: none;">support@finarchitect.site</a>.
                                    </p>
                                    <p style="font-size: 16px; line-height: 1.5;">Best Regards,</p>
                                    <p style="font-size: 16px; line-height: 1.5;">The Finarchitect Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 14px; color: #888;">
                                    <p style="margin: 0;">&copy; 2025 Finarchitect. All rights reserved.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    }

    email = resend.Emails.send(params)

    
def newUpdate(user):
    params: resend.Emails.SendParams = {
    "from": "Finarchitect <updates@finarchitect.site>",
    "to": [f"{user['email']}"],
    "subject": "Exciting News: Introducing Our New Financial Model",
    "html": f"""
        <html>
        <body>
            <h1>Exciting News: Introducing Our New Financial Model!</h1>
            <p>Dear {user['first_name']},</p>
            <p>We're thrilled to announce the launch of our latest financial model, designed to provide you with even more precise and insightful financial planning and analysis.</p>
            <p>Here's what you can expect from the new model:</p>
            <ul>
            <li><strong>Enhanced Accuracy:</strong> Leveraging advanced algorithms for more precise forecasts.</li>
            <li><strong>Improved User Interface:</strong> A more intuitive and user-friendly experience.</li>
            <li><strong>New Features:</strong> Additional tools and functionalities to better meet your needs.</li>
            </ul>
            <p>We believe this update will significantly enhance your financial planning experience and help you achieve your financial goals more effectively.</p>
            <p>We're always here to help you get the most out of our services. If you have any questions or need assistance, feel free to reach out to our support team at <a href="mailto:support@finarchitect.site">support@finarchitect.site</a>.</p>
            <p>Thank you for being a valued member of the Finarchitect community. We look forward to continuing to support your financial journey.</p>
            <p>Best Regards,</p>
            <p>The Finarchitect Team</p>
        </body>
        </html>
    """
    }

    email = resend.Emails.send(params)


def forgotPassEmail(data):
    resetLink = f"https://reset-password-jet.vercel.app/{data['uid']}/{data['token']}"
    params: resend.Emails.SendParams = {
        "from": "Finarchitect <support@finarchitect.site>",
        "to": [f"{data['email']}"],
        "subject": "Reset Your Finarchitect Password",
        "html": f"""
            <html>
            <body>
                <h1>Password Reset Request</h1>
                <p>Dear {data['first_name']},</p>
                <p>We received a request to reset your password for your Finarchitect account. Click the link below to reset your password:</p>
                <p><a href="{resetLink}" style="
                    background-color: #007bff;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin: 20px 0;
                ">Reset Password</a></p>
                <p>If you did not request a password reset, please ignore this email. Your password will remain unchanged.</p>
                <p>For security reasons, this link will expire in 24 hours.</p>
                <p>If you have any questions or need further assistance, feel free to contact our support team at <a href="mailto:support@finarchitect.site">support@finarchitect.site</a>.</p>
                <p>Best Regards,</p>
                <p>The Finarchitect Team</p>
            </body>
            </html>
        """
    }
    
    email = resend.Emails.send(params)


def anyUpdate(user, updateName, link):
    params: resend.Emails.SendParams = {
    "from": "Finarchitect <updates@finarchitect.site>",
    "to": [f"{user['email']}"],
    "subject": "Exciting News: Introducing Our New Financial Model",
    "html": f"""
        <html>
        <body>
            <h1>Exciting News: Introducing Our New Financial Model!</h1>
            <p>Dear {user['first_name']},</p>
            <p>We're thrilled to announce the launch of our latest financial model, designed to provide you with even more precise and insightful financial planning and analysis.</p>
            <p>Here's what you can expect from the new model:</p>
            <ul>
            <li><strong>Enhanced Accuracy:</strong> Leveraging advanced algorithms for more precise forecasts.</li>
            <li><strong>Improved User Interface:</strong> A more intuitive and user-friendly experience.</li>
            <li><strong>New Features:</strong> Additional tools and functionalities to better meet your needs.</li>
            </ul>
            <p>We believe this update will significantly enhance your financial planning experience and help you achieve your financial goals more effectively.</p>
            <p>We're always here to help you get the most out of our services. If you have any questions or need assistance, feel free to reach out to our support team at <a href="mailto:support@finarchitect.site">support@finarchitect.site</a>.</p>
            <p>Thank you for being a valued member of the Finarchitect community. We look forward to continuing to support your financial journey.</p>
            <p>Best Regards,</p>
            <p>The Finarchitect Team</p>
        </body>
        </html>
    """
    }

    email = resend.Emails.send(params)


def modelGuide(user):
    link = "https://finarchitect.site"
    params: resend.Emails.SendParams = {
        "from": "Susan from Finarchitect <guide@finarchitect.site>",
        "to": [user],
        "subject": "Your Financial Modeling Guide (As Requested)",
        "html": f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
                <p>Hi there,</p>
                
                <p>Here's the financial modeling guide you requested. It covers key concepts and practical steps to help you build robust financial models for better decision-making.</p>
                
                <p><strong>Access your guide with one click:</strong></p>
                
                <table align="center" cellpadding="0" cellspacing="0" style="margin: 20px auto;">
                    <tr>
                        <td align="center" style="border-radius: 4px;" bgcolor="#2563eb">
                            <a href="{link}" target="_blank" style="font-size: 16px; font-family: Arial, sans-serif; color: #ffffff; text-decoration: none; border-radius: 4px; padding: 12px 24px; border: 1px solid #2563eb; display: inline-block; font-weight: bold;">
                                View Financial Modeling Guide
                            </a>
                        </td>
                    </tr>
                </table>
                
                <p>If you'd like a walkthrough or have questions, reply to this email—I'm happy to help.</p>
                
                <p>Best regards,<br>
                Susan<br>
                Finarchitect Team</p>
                
                <p style="font-size: 0.9em; color: #666;">
                    P.S. If you didn't request this guide, let us know so we can update our records.
                </p>
            </body>
            </html>
        """
    }
    email = resend.Emails.send(params)