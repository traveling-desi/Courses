Dear Student, 

This week is tricky and fiddly. Please read this carefully... 

We have made a couple of changes since the films were made, 
which make things work better on mobile Safari. But you 
have the complete source code etc. here. 

------
Android users note: 
this is javascript mode only. It will not work in Android mode
BUT! it should work in your Android browser, just like iOS and Desktop OS
BUT! in our tests, the javascript FileReader is not available in Android <= 2.3
     so you can't import from the camera in older Android versions with this code

------

Here you have two folders:

source_code
put_on_your_web_server

To make it work for you, go into put_on_your_web_server
* edit insta.js, putting in your own fb app id
* save and then put the files onto your web server
* create a folder called upload in the same folder on your web server
* give Apache permissions to write to that folder
  (chmod command in FTP client -> chmod  777 upload, for example)
* note the publish to fb will only work if your web server
  is a real web server visible from the internet
  and if you put in the address of that web server to the 
  app info page on facebook

To make a custom version:
* edit the source_code/InstaSpamFinal project in Processing/ javascript mode
* do an export. 
* copy the InstaSpamFinal.pde file ONLY from the folder (plus image files if needed) 
  up to the web server. 

Have fun, drop into the forums for help. 
