"""
1. Allow Less secure app access in your google account from which you have to send email.
                        > Go to https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4Plwu-lxDuRfaAp_sMWewHvZ27O1MtZjJ9cXQJfFSUHKpCxGaQ3xqihupRn9Ae_CjS8i1cWG1LfJteHLrSgI4wyMlP_5Q
                        > Login with the email that you have to used [It must be same that you have used in environment variable]
                        > Turn it on

                    
                    > Follow this link if your are facing issues : https://www.dev2qa.com/how-do-i-enable-less-secure-apps-on-gmail/#:~:text=1.%20Turn%20On%20Allow%20Less%20Secure%20Apps%20Access%20Google%20Account%20Steps

2. Start your mysql server .

                Suggested IDE : Pycharm or Python IDLE

3. Please change font size in Python IDLE to 7 if you are using it,fir better experience.
                   > Open IDLE
                   > Click Options
                   > Click Configure IDLE
                   > You will find size block in bottom left corner
                   > If it is 7 don't change it and if it is not 7 ,Please change it to 7.
"""


def email():
    return "ENTER YOUR EMAIL ID FROM WHICH YOU HAVE TO SEND EMAIL TO USER"


def email_password():
    return "ENTER THE PASSWORD OF THE EMAIL ID MENTIONED ABOVE"


if __name__ == "__main__":
    email()
    email_password()
