
// This is a slightly more developed
// version of the instaspam sketch
// It does not have the camera, PHP
// or facebook functions integrated yet
// so you can start with this
// if you want to do that integration yourself

/* @pjs preload="synthesizer.jpg"; */

// the image that is being edited
PImage originalImage;

// images to use for button logos
PImage facebookLogo, cameraLogo, rotateLogo;

// the overlay images that can be applied to the image
PImage [] overlays;
// images for the tint buttons
PImage [] tintImages;

// the tint colors we can apply
color [] tints; 

// radio buttons to trigger tints and overlays
RadioButtons tintButtons;
RadioButtons overlayButtons;

// button to load a file from the camera or file
Button fileButton;
// button to post to Facebook
Button FBButton;

Button rotateButton;

// whether the user interface is showing
boolean displayGUI = false;

// this stops you showing a file temporarily as
// we load a new file
boolean updateImage = false;

// post to facebook next frame
boolean post = false;

// the angle of rotation of the image
float angle = 0;

// the position of the center of the image, 
// this allows you to scroll it around
int imageCenterX;

// loads a new image when you get one from the camera
void setImage(String url) {
  //console.log("loading: "+url);
  originalImage  = loadImage(url);
  updateImage = true;
  loop();
}

void setup()
{
  size(480, 640);

  imageCenterX = width/2;
  originalImage = loadImage("synthesizer.jpg");
  facebookLogo = loadImage("asset.f.logo.lg.png");
  cameraLogo = loadImage("cameraLogo.png");
  rotateLogo = loadImage("rotateLogo.png");

  tints = new color[4]; 
  tints[0] = color(0, 255, 100);
  tints[1]= color(120, 100, 0);
  tints[2] = color(0, 100, 160);
  tints[3] = color(160, 60, 10);

  tintImages = new PImage[4];
  tintImages[0] = loadImage("tintImage0.png");
  tintImages[1] = loadImage("tintImage1.png");
  tintImages[2] = loadImage("tintImage2.png");
  tintImages[3] = loadImage("tintImage3.png");

  overlays = new PImage[2];
  overlays[0] = loadImage("overlay1.png");
  overlays[1] = loadImage("overlay2.png");

  overlayButtons = new RadioButtons(overlays.length, 10, height-50, 64, 48, HORIZONTAL); 
  for (int i = 0; i < overlays.length; i++)
  {  
    // sets the image for the button to be the same as the overlay itself
    overlayButtons.setImage(i, overlays[i]);
    // sets the colors to use for the outline
    // the inactive color is transparent so the border is invisible
    overlayButtons.buttons[i].setInactiveColor(color(255, 255, 255, 0));
    overlayButtons.buttons[i].setActiveColor(color(255));
  }

  tintButtons = new RadioButtons(tints.length, 100, height-50, 64, 48, HORIZONTAL); 
  for (int i = 0; i < tints.length; i++)
  {
    // sets the image for the button to be the same as the main image
    tintButtons.setImage(i, tintImages[i]);
    // set a tint for the button to be the same as tint i
    //tintButtons.buttons[i].setImageTint(tints[i]);
    // sets the colors to use for the outline
    // the inactive color is transparent so the border is invisible
    tintButtons.buttons[i].setInactiveColor(color(255, 0));
    tintButtons.buttons[i].setActiveColor(color(255));
  }

  // create buttons for file loading and facebook posting
  // load logos for each

  rotateButton = new Button ("rotate", width-130, height-50, 36, 36);
  rotateButton.setImage(rotateLogo);
  fileButton = new Button ("file", width-90, height-50, 36, 36);
  fileButton.setImage(cameraLogo);
  FBButton = new Button ("FB", width-40, height-50, 36, 36);
  FBButton.setImage(facebookLogo);
}

void draw()
{
  background(100);

  // don't display the image if you have just updated the image
  if (! updateImage)
  {
    pushStyle();
    // if we have selected a tint tintButtons.get will be positive
    // if so apply a tint

    if (tintButtons.get() >= 0)
    {
      tint(tints[tintButtons.get()]);
    }

    // rescale the image so that it is the full height of the screen
    float imageWidth = (height*originalImage.width)/originalImage.height;

    // draw the image
    imageMode(CENTER);
    pushMatrix();
    translate(imageCenterX, height/2);
    rotate(angle);
    image(originalImage, 0, 0, imageWidth, height);
    popMatrix();
    // turn the tint off for the overlay

    // if we have selected a tint tintButtons.get will be positive
    // if so draw the overlay
    if (overlayButtons.get() >= 0)
    {
      image(overlays[overlayButtons.get()], width/2, height/2, width, height);
    }
    popStyle();


    // if we are displaying the user interface, draw it
    if (displayGUI)
    {
      // draw a transparent rectangle behind the UI to make it
      // more visible
      pushStyle();
      fill(0, 128);
      noStroke();
      rect(0, height - 60, width, 60);


      // draw all the UI elements
      tintButtons.display();
      overlayButtons.display();
      FBButton.display();
      fileButton.display();
      rotateButton.display();
      noTint();
      popStyle();
    }
    // post is set to true
    // when the user hits the facebook button
    if (post)
    {
      // we call click on the hidden yada button
      // which is a bit of voodoo
      // to make mobile safari play nicely! 
      $("#yada").click();
      post = false;
    }
  }
  else // if we are updating the image, just draw some text
  {
    textAlign(CENTER, CENTER);
    text("updating", width/2, width/2);
    // stop the update message once we have drawn it once
    float imageWidth = (height*originalImage.width)/originalImage.height;

    originalImage.resize(imageWidth, height);
    updateImage = false;
  }
}

// respond to user interface events
void mouseReleased()
{
  // first we need to check if the user interface is show
  // if it is we can trigger events. Otherwise the click
  // will show the interface
  if (displayGUI)
  {
    // if we are in the interface area at the bottom of the 
    // screen we trigger the UI events
    if (mouseY > height - 60)
    {
      tintButtons.mouseReleased();
      overlayButtons.mouseReleased();

      if (FBButton.mouseReleased())
      {
        //      println("hello");
        // we delay the posting to facebook so that we can 
        // hide the interface before we post it! 
        // so se set this variable to true
        // hude the GUI, then post... see the draw method
        post = true;
        displayGUI = false;
      }
      if (fileButton.mouseReleased())
      {
        println("now we call selectFile, defined in insta.js");
        // note that this function selectFile
        // is defined in insta.js
       selectFile();

        displayGUI = false;
      }
      if (rotateButton.mouseReleased())
      {
        angle += radians(90);
        displayGUI = false;
      }
    }
    //else  
    {
      // if we clicked in the middle of
      // the screen, hide the UI
      displayGUI = false;
    }
  }
  else
  {
    // if the UI was hidden, a click will show it
    displayGUI = true;
  }
}

// when we dragg we can move the image from left to
// right (it is the full screen height so we don't want
// to move it up and down)
void mouseDragged()
{
  imageCenterX += mouseX - pmouseX;
}


