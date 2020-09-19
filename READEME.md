(Python - Django and Multiprocesssing, Javascript, HTML, CSS, Heroku)

Using Beautiful Soup, the program searches for the BBC webpoage for each specific catagory, 
it then looks for the first 5 articles published today in reverse chronological order. 
Next it finds the title of the page by specifically looking at the classNames of each heading. 
Finally, it finds all of the <p> paragraph tags, which contain the content of the webpage.

Text found in paragraph tags is then appended to a single string, with commonly occuring strings of information removed. 
An example of this is "Share this withEmailFacebookMessengerMessengerTwitterPinterestWhatsAppLinkedInCopy this linkThese are external links and will open in a new window". 
I explain why this is important in the Extractive Summarising Algorithm box.

This summarising algorithm was developed by Matthew Mayo. The algorithm works by dividing a text into sentences and giving them a score. 
This score determines how important the information is by weighting different features such as: rarity of words, word length and sentence length. 
It is therefore, important that we syntactically clean the information, 
since information that needs to be cleaned will score highly since it is often long, nonsensical gibberish!

This project runs on Django, a web development framework in Python. It allows us to create dynamic webpages using HTML, CSS, Javascript and Python. 
Using Django, we can drastically reduce the number of files needed for this project to work by reusing HTML templates, 
and using a langauge called Jinja to dynamically input the titles and summaries of each news catagory.

