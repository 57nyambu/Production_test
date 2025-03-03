import resend
from Root.settings import base

resend.api_key = base.RESEND_KEY


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


def modelGuide(email):
    link = "https://finarchitect.site"
    params: resend.Emails.SendParams = {
    "from": "Finarchitect <guide@finarchitect.site>",
    "to": [email],
    "subject": "Your Guide to Financial Modeling",
    "html": f"""
        <html>
        <body>
            <h1>Your Guide to Financial Modeling</h1>
            <p>Financial modeling is an essential tool for making informed business decisions and planning for the future. 
            Whether you're a seasoned financial professional or new to the world of finance, our comprehensive guide will help you navigate the intricacies of financial decisions
            with our statistical based financial models.</p>
            <p>Click the link below to access your free guide:</p>
            <p><a href="{link}" style="
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                margin: 20px 0;
            <p>If you have any questions or need assistance, 
            <p>feel free to reach out to our support team at <a href="tom@finarchitect.site">Support</a></p>
            <p>Best Regards,</p>
            <p>The Finarchitect Team</p>
        </body>
        </html>
    """
    }
    email = resend.Emails.send(params)
