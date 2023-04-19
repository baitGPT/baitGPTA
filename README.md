## BaitGPT : Automated emails with scammers using GPT3.5

French documentation [there](/readme_fr.md)
With the recent progress of Large Language Models and their wider usage from the general publics, many have feared an increase usage of these for scamming purposes [1](https://www.mcafee.com/blogs/internet-security/chatgpt-a-scammers-newest-tool/)[2](https://medium.com/geekculture/chatgpt-the-new-frontier-of-scamming-and-fraud-6884da6e2ff1). While this is a risk, the purpose of this project is to test the opposite : using AIs to flood scammers and catfishes with automated answers.

At this point, the project aims at scam emails such as the advance-fee scams, catfishes, or other impersonations.

This idea is not new, and has been attempted humorously by James Veitch in his [Youtube series](https://www.youtube.com/playlist?list=PLjaZD_N3WCf-SzY9lQqsUNbubksD_KCPT).

The goal of this project is to automate the process in the hope of fighting efficiently against scams.

### How to use BaitGPT?
#### As a user :
- Go through your mailbox (and spam folder) and identify scams that fit the project (Potentially from advance-fee scams, catfishes, or other impersonations. Phishing emails requesting to click on a link or open an attachment are not included.).
- Download the identified emails as `.eml` files (Tutorial for [Gmail and Outlook](https://www.codetwo.com/kb/export-email-to-file/#outlook-on-the-web)).
- Send an email to [BaitGPT.reports@outlook.com](mailto:BaitGPT.reports@outlook.com?subject=[GitHub]%20Scams%20report)], with attached the `.eml` files.
- Delete the `.eml` files from your computer.
#### As a sender :
- clone the repository
- get an [api key](https://platform.openai.com/account/api-keys) from OpenAI store it in `GPTkey.json` as `{"api_key": "Your_Key"}`.
- Create multiple email addresses, and get the associated connection into `credential_head.json` and `credential.json` as `{"users" : [{"email" : "example@outlook.com", "password" : "safe_password", "imap_server" : "outlook.office365.com", "smtp_server" : "smtp-mail.outlook.com", "smtp_port" : 587}]}`. The head is the email address that gathers the emails, others are the one that send the answers and maintain the discussion.
- For safety concerns (downloading attachments and sending fake emails to scammers), use a remote environment for execution.
### How does it work ?
- First, scam emails are retrieved from the head mailbox.
- Then for each email, its text-body is extracted, as well as header info necessary for the response.
- GPT3.5 is called a first time to assess if it looks like a scam email. In case of negative response or doubt, the email is ignored.
- A response email is crafted with GPT3.5, following a customized prompt that can be adapted.
- One of the "output" mailbox sends the response email trying to respect email RFC conventions.
- At any of these steps, human verification can be added (and is currently active before sending).
- Independently, a similar loop runs on "output" mailbox in order to continue discussion in case the bait works.
### Q&A
- **What do we do of your data ?**
Temporary, email can be temporary stored for debugging and efficiency assessment.
Your data (email address and personal info contained in the emails) will not be exploited or shared with any third party.
Emails are deleted after being answered and doesn't contain your email address. Only the body of the document is sent, which may contain personal information such as names or leaked credentials.
- **How much does it cost ?**
To the user : nothing. To the sender : about $0.003 per email. To the scammers : precious time not spent on scamming real people.
### Further development:
Among all the scams, the one addressed here is only a minor share, next to phishing, malicious attachments, etc. The primary goal of this project is to assess the efficiency of such a method. Any idea of improvement is welcomed.

One of the main limitation is the medium : emails seems deprecated compared to private messengers on social networks such as Instagram or Facebook. Implementation on these media would open possibilities but represent a huge step in term of complexity.
