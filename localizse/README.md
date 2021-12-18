# Localizse:Transtech

## Intro

This app is a prototype for a crowd-sourced translation service specifically geared towards translating 'technical content' or, in other words, content that involves LaTeX in some way.

The idea for this app was inspired by a specific gap in the workflow to translate content at the company I work at.

The aim is to efficiently translate short-form content containing mathematical expressions through the use of automatic translation and human review from a crowd. This could also be easily adapted to utilise contract workers.

## Distinctiveness and Complexity

#### **Distinctivness**

This app is centred around two main aspects:

-   the translation service
-   and crowd sourcing.

None of the projects in the CS50W 2021 course involved these elements. Admittedly, there is a small amount of overlap in the communication functionality with Project 3: Mail. Other than that and some inspiration from the methodology in the other projects, this project is distinct.

#### **Complexity**

The aspects which make this project distinct are also from where it draws its additional complexity.

The translation is initially automatically done by an API. These types of automatic translations do not handle LaTeX or other symbolic mark-up schemes well, so these sections of the input are factored out and replaced back into the content for review. A more complex model structure is required to keep a track of all the information about original versions and their translations.

The crowd sourcing involves various aspects:

-   Onboarding
-   Work assignment
-   Input control
-   Fraud detection
-   Promotion
-   Accuracy monitoring and finance

Onboarding requires correctly registering the new user with relevant information in a consistent format. Work assignment uses this information to pull corresponding items from the available work. There are various forms of input control to make sure that users do not submit badly formatted data and to alleviate the need to have familiarity with LaTeX. Fraud detection is in place to make sure users are actually doing work and will otherwise get locked out of the system. Promotion to a higher position is achieved through an exchanging of unique keys through an 'offer/accept' flow. There is additional information for the user in the form of accuracy information and details of their earnings.

## Files by folder

**db.sqlite3**
: the database file

**requirements.txt**
: the required python libraries for the project. Automatically generated with `pip freeze > requirements.text`

### keys/

**localizse-18660e5baf67.json**
: The key information for the Google Translate API

**localizse-18660e5baf67.json:Zone.Identifier**
: auto-generated file for API key

### localizse/

**settings.py**
: the only changes here are to change the `AUTH_USER_MODEL`, the `TIME_ZONE`, and to add the `add_badge` processor.

**urls.py**
: the only change here is to add the transtech urls.

### transtech/

**admin.py**
: Models are registered here.

**models.py**
: where the models are defined. We have

-   Language - contains the name and ISO 639-1 language code of a given language.
-   User - based on `AbstractUser` with additonal fields for languages and crowd management.
-   TechContent - An 'empty' model which serves to group together the original content and its translated versions.
-   TechContentVersion - where most of the data is stored, these contain the actual content and the metadata required to identify them by language and status.
-   Item - represents a piece of work, either review or audit, with fields for the worker, a timestamp and a comparison of the content for measuring accuracy.
-   Report - a model to allow users to report issues with the content.
-   Message - how communication is treated in the database. A Message with a null recipient is an announcement.

**processor.py**
: defines a context processor to show an unread messages badge to the layout template without having to pass it in with every request.

**trnslt.py**
: defines the functions to translate the tech content through the Google Translate API

**urls.py**
: registers the available URLS

**views.py**
: defines the app's views.

-   accept() - allows a user to accept their promotion offer, checking their offer key against the one in the URL.
-   account() - processes and passes the info required for the _account_ page.
-   index() - returns the _landing_ page, or the login page if the user is not authenticated.
-   log() - passes the information for the full work log to the _work log_ page.
-   login_view() - Where the user can login
-   logout*view() - the user is logged out and sent to the \_login* page.
-   messages() - Where the user can view their messages.
-   message() - is called from the _messages_ page to get the content for the message modal.
-   offer() - handles a POST to update the offer field of a user and send them an offer message.
-   register() - handles the _register_ page and the POST request to register an new user.
-   report() - adds a content `Report` to the database.
-   save() - Used to save new content or edited content. This has logic to deal with each case correctly.
-   set_lang() - handles a POST request to change the users active languages.
-   update() - handles a POST request to change the users personal details.
-   users() - Where staff can see a list of users and offer them a promotion.
-   work_switch() - determines which type of work a user should be directed to.
-   work() - takes the user to the corressponding work page, with logic to stop users from accessing the wrong type of work.
-   set_langs() - A helper function to set the users default active languages.

### transtech/static/transtech/

**acc-scripts.js**
: the scripts that run on the _account_ page. These allow for the user to edit their personal information and imposes some input control on the language selection.

**csrf-cookie.js**
: this reads the Django csrf token which can then be passed into JS fetch requests.

**gen-scripts.js**
: these scripts run on most pages and control the behaviour to display and update the users active languages in the navigation bar.

**msg-scripts.js**
: this runs on the _messages_ page and allows for a selected message to be displayed in full in a model and also updates the document to display the just opened message as read.

**new-scripts.js**
: this runs on the _create_ page and defines the interface for inputting new content: drawing on the KaTeX library to render the delimited LaTeX in the input. There is also input control and the ability to edit recently submitted content.

**reg-scripts.js**
: this runs on the _register_ page to ensure the required information is input correctly, giving feedback to the user if they make a mistake.

**rev-scripts.js**
: Perhaps the most involved script this runs on the _review_ page and contains logic to factor our the LaTeX in a piece of content and provide an interface where the user can insert the labelled expressions with a tag, avoiding the need to interact directly with the LaTeX code. This also provides the ability to edit recent submission. This runs on the audit page almost identically with a slight change to the interface since the editing field is not necessary by default.

**styles.css**
: Contains the various styles of the customised elements.

**usr-scripts.js**
: this runs on the _users_ page (only accessible by staff) and allows promotion offers to be made.

### transtech/templates/transtech/

**account.html**
: displays various information about the current user, including personal details, financial details and a truncated work log.

**audit.html**
: The page where auditing takes place, an Auditor checks reviewed content and makes edits as necessary. The content pulled is a random choice based on the active languages of the Auditor. This requires the KaTeX library.

**create.html**
: A view to create new content. This exists more for the testing of the application, the general approach in a real-world application would be to import a batch of content that needs translating from a client and have the crowd work on it before returning the translation. In any case, this has an interface to input and render content involving LaTeX and submit it to the database.

**index.html**
: The landing page. Here users can see announcements and other info about the application

**layout.html**
: defines the navigation bar and a couple interactive elements, such as the badge display for unread messages and the active languages selector. This is also where Bootstrap is loaded.

**log.html**
: displays a full work log for the logged in user

**login.html**
: An interface to login. Displays an error message when necessary

**message.html**
: This is a template for the modal content used to display open messages

**messages.html**
: A page to display messages sent to the user.

**register.html**
: defines the form to intially register the user.

**report.html**
: A template to produce the report modal available on the _review_ and _audit_ pages

**review.html**
: provides the review interface for a Reviewer in a similer way to `audit.html`. This also requires the KaTeX library.

**users.html**
: provides a list of users to allow promotion offers to be made.

**workerror.html**
: A template that is returned when the query to choose the next work item comes up empty.

## How to run

Run the command `python manage.py runserver` (or with `python3` if you do not have `python-is-python3` installed).

In order to add new content you will need to create a superuser with `python manage.py createsuperuser` and login at the local server address + `/admin`. The create interface is only available to staff and users in the Creator group.

If you decide to run from a clean database you will need to add the languages and groups (Creator, Reviewer, Auditor) manually in admin. (The most important part here is to use a valid [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for the languages.)

## Additional information

The Google Translate API is a paid service, so please go easy on the testing.
