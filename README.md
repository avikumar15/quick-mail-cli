
# Quick Email CLI

A command line interface to send mail without any hassle.

## Why this tool?

Sending last minute mails using conventional tools can get annoying and tiresome. This CLI helps in such situation since it makes sending mail hassle-free and very quick. Use this tool to send mails quickly without leaving your terminal.

## Installation

#### Debian

```
$ git clone https://github.com/<USER_NAME>/quick-email-cli

* add line export PYTHONPATH=/path/to/project/quick-email-cli to ~/.bashrc *

$ cd quick-email-cli/

* activate virtual environment *

$ pip install -r requirements.txt
$ pip install .
```

Check installation by running


```
$ quickmail --version
```

## Usage


To use this:

	$ quickmail --help

<h3></h3>

```
usage: quickmail [-h] [-v] {clear,init,send,template} ...

A command line interface to send mail without any hassle

positional arguments:
  {clear,init,send,template}
    clear               clear the body of message from local or even the token if
                        --justdoit argument is added
    init                initialise token and set your email id
    send                send the mail
    template            manage templates of mail body

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print current cli version

```


Create your [OAuth client ID](https://console.developers.google.com/apis/credentials/) and select app type as Desktop App and download the credentials.json file.
<h2></h2>

Then run the init command to authenticate gmail, and generate token. This command is required to be run only once.

```
$ quickmail init <path/to/credentials.json>
```

Now you are all set. Use the send command to send mail.


	$ quickmail send --help

<h3></h3>

```
usage: quickmail send [-h] -r RECEIVER -sub SUBJECT [-t TEMPLATE] [-b BODY]
                      [-a ATTACHMENT] [-l]

Use the send command to send mail. Body can be passed as an argument, or typed in
a nano shell. Use optional --lessgo command for sending mail without confirmation

optional arguments:
  -h, --help            show this help message and exit
  -r RECEIVER, --receiver RECEIVER
                        receiver's email address, eg. '-r "xyz@gmail.com"'
  -sub SUBJECT, --subject SUBJECT
                        email's subject, eg. '-sub "XYZ submission"'
  -t TEMPLATE, --template TEMPLATE
                        template of email body, eg. '-t="assignment_template"'
  -b BODY, --body BODY  email's body, eg. '-b "Message Body Comes Here"'
  -a ATTACHMENT, --attachment ATTACHMENT
                        email's attachment path, eg. '~/Desktop/XYZ_Endsem.pdf'
  -l, --lessgo          skip confirmation before sending mail

```

Body and attachments are optional arguments. Body can be either passed as an argument otherwise it can also be typed in the nano shell (Use -t argument to use a template body). Use the --lessgo (shorthand -l) to skip confirmation of mail, for quicker mail deliveries.

To clear the cli storage, use the clear command. Use --justdoit (shorthand -j) to even remove the credential and token files from project directory, this extra argument would allow you to change your primary email address.


	$ quickmail clear --help

<h3></h3>

```
usage: quickmail clear [-h] [-j]

Use the clear command to clear all email body that are saved in your home
directories. Additionally, pass --justdoit to remove the credential files as well

optional arguments:
  -h, --help      show this help message and exit
  -j, --justdoit  clear storage including the credentials and token

```

To manage templates use the template command.

	$ quickmail template --help
	
<h3></h3>

```
usage: quickmail template [-h] {add,listall,edit} ...

manage mail templates

positional arguments:
  {add,listall,edit}
    add               add a new template
    listall           list all templates
    edit              edit a particular template

optional arguments:
  -h, --help          show this help message and exit

```

Following is a recording of the terminal session which records the usage of `quickmail` from init command till send command. 

<h3></h3>

[![asciicast](https://asciinema.org/a/78mPkSTa0rTK3TXhnkgRDP6RO.svg)](https://asciinema.org/a/78mPkSTa0rTK3TXhnkgRDP6RO)

### Improvements and Bugs

Found any bugs? Or have any suggestions, feel free to open an issue.

