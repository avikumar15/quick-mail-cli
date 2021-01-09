## Quick Email CLI

A command line interface to send mail without any hassle.

### Why this tool?

Sending last minute mails using conventional tools can get annoying and tiresome. This CLI helps in such situation since it makes sending mail hassle-free and very quick. Use this tool to send mails quickly without leaving your terminal.

-------------------------

### Installation

#### Debian

```
$ git clone https://github.com/<USER_NAME>/quick-email-cli
$ cd quick-email-cli/

* activate virtual environment *

$ pip install -r requirements.txt
$ pip install -e .
```


Check installation by running


```
$ quickmail --version
```

-------------------------

### Usage


To use this:

	$ quickmail --help


```
usage: quickmail [-h] [-v] {clear,init,send} ...

A command line interface to send mail without any hassle

positional arguments:
  {clear,init,send}
    clear            clear the body of message from local or even the
                     token if --justdoit argument is added
    init             initialise token and set your email id
    send             send the mail

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      print current cli version
```


Create your [OAuth client ID](https://console.developers.google.com/apis/credentials/) and download the credentials.json file.
Then run the init command to authenticate gmail, and generate token.

```
$ quickmail init <path/to/credentials.json>
```

Now you are all set. Use the send command to send mail.


	$ quickmail send --help

```
usage: quickmail send [-h] -r RECEIVER -sub SUBJECT [-b BODY]
                      [-a ATTACHMENT] [-l]

Use the send command to send mail. Body can be passed as an argument,
or typed in a nano shell. Use optional --lessgo command for sending
mail without confirmation

optional arguments:
  -h, --help            show this help message and exit
  -r RECEIVER, --receiver RECEIVER
                        receiver's email address, eg. '-r
                        "avithewinner1508@gmail.com"'
  -sub SUBJECT, --subject SUBJECT
                        email's subject, eg. '-sub "CA Endsem
                        Submission'"
  -b BODY, --body BODY  email's body, eg. '-b "Message Body Comes
                        Here"'
  -a ATTACHMENT, --attachment ATTACHMENT
                        email's attachment path, eg.
                        '~/Desktop/CA_Endsem.pdf'
  -l, --lessgo          skip confirmation before sending mail
```

Body and attachments are optional arguments. Body can be either passed as an argument otherwise it can also be typed in the nano shell. Use the --lessgo (shorthand -l) to skip confirmation of mail, for quicker mail deliveries.

To clear the cli storage, use the clear command. Use --justdoit (shorthand -j) to even remove the credential and token files from project directory.


	$ quickmail clear --help
	
```
usage: quickmail clear [-h] [-j]

Use the clear command to clear all email body that are saved in your
home directories. Additionally, pass --justdoit to remove the
credential files as well

optional arguments:
  -h, --help      show this help message and exit
  -j, --justdoit  clear storage including the credentials and token
```

-------------------------

Following is a recording of the terminal session which records the usage of `quickmail`. \

[![asciicast](https://asciinema.org/a/5B8bdkDSp6rXjqo6feVbRSrMw.svg)](https://asciinema.org/a/5B8bdkDSp6rXjqo6feVbRSrMw)

-------------------------

### Improvements and Bugs

Found any bugs? Or have any suggestions, feel free to open an issue.

