# BookDiary - vot
Web application where you can add all the books you've read. You add the books with title, author, genre and you can add a comment about what you thought about the plot and all that book nerdy stuff. You can also see the list of books you've added. In this list you can search for a book by it's genre or a title, in this way if you've read the same book a few times you can see how your view about the book changed.
The application is written in python using python flask. The web pages are .html files. The prototype databse is written in SQLlite and it is used for tasting if everything else works as expected. 
The idea is that this web app will be used from Microsoft azure. For now i have everything put in an azure blob container and the index.html page opens. The page where you write the information about the book you want to add works perfect, all good, until you click the "add book" button. Here occurres the problem that the page can't acces the database. We need azure database to be connected to the static web app so we can use it and add our books and then displey them.

(if you are reading this the azure database did not happened and the app works only from local host)
Well... it didn't work in the azure thingy but i made it pretty and i have the correct connections with the azure database but for some reason it still cannot add or get from the databse... in azure i bassicaly have no database. BUT it works perfectly from the local host :)
