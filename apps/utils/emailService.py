import resend
from Root.settings import base

resend.api_key = base.RESEND_KEY
#user_data={'email':'mwakionyambu57@gmail.com', 'first_name':'Tom5',}

def welcomeEmail(user):
    params: resend.Emails.SendParams = {
    "from": "Finarchitect <welcome@finarchitect.site>",
    "to": [f"{user['email']}"],
    "subject": "Welcome to Finarchitect!",
    "html": f"""
        <html>
        <body>
            <h1>Welcome to Finarchitect!</h1>
            <p>Dear {user['first_name']},</p>
            <p>We are thrilled to have you with us. Thank you for signing up and becoming a part of the Finarchitect community!</p>
            <p>At Finarchitect, we strive to provide you with the best financial architecture solutions tailored to your needs.</p>
            <p>Here are some next steps to get you started:</p>
            <ul>
            <li>Explore your dashboard and familiarize yourself with the features.</li>
            <li>Connect your accounts and start managing your finances efficiently.</li>
            <li>Check out our resource center for tips and best practices.</li>
            </ul>
            <p>If you have any questions or need assistance, feel free to reach out to our support team at <a href="mailto:support@finarchitect.site">support@finarchitect.site</a>.</p>
            <p>Best Regards,</p>
            <p>The Finarchitect Team</p>
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


def forgotPassEmail(user, resetLink):
    params: resend.Emails.SendParams = {
    "from": "Finarchitect <support@finarchitect.site>",
    "to": [f"{user['email']}"],
    "subject": "Reset Your Finarchitect Password",
    "html": f"""
        <html>
        <body>
            <h1>Password Reset Request</h1>
            <p>Dear ,</p>
            <p>We received a request to reset your password for your Finarchitect account. Click the link below to reset your password:</p>
            <p><a href="{resetLink}" target="_blank">Reset Password</a></p>
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