# Whats-Fishy:
 Identify phishing emails based on ML and NLP


1. Install the dependencies using pip install -r requirements.txt
2. Go to command prompt, open python console and run the following commands:
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
2. Get the Gmail API key and store it in credentials.json
3. Run the program using python main.py
4. A dialog box will pop up, allowing you to remove the phishing emails from your inbox.
5. Sign in to your gmail account and allow access to What's Fishy to view and modify your emails.
6. The phishing emails will be moved to trash, along with an email informing you about the same.

The model used for classifying emails and URLs is the Random Forest classifier. It has an accuracy of 99% in the case of emails and of 90% in the case of URLs. The datasets used are from Kaggle. The GUI is developed using Python's PyQt5. Based on the results of the email classifier and those of the hyperlinks present in the email, a decision is taken. The various parameters included are the vocabulary richness of the emails, presence of function words, number of hyperlinks in an email, etc. For the URL classifier, some of the features are use of URL shortening services, having a sub-domain, presence of IP address in the URL, double slash redirecting, etc. These parameters can be seen in the respective datasets phishing_mails.csv and phishing_url.csv . After launching the program, a button redirects the user to the Gmail sign-in to provide permission to view and modify the emails. Thereafter, the program retrieves the unread emails and predicts its class, based on which the email is moved to trash if it is found to be phishing. The Gmail API is used for retrieving the emails. 