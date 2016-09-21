//The MIT License (MIT)

//Copyright (c) 2013 Mick Grierson, Matthew Yee-King, Marco Gillies

//Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
//The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import processing.video.*;
Movie myMovie;

int currentFrame = -1;

String fileName = null;

void setup() {
  size(420, 280);
  selectInput("Select a file to process:", "fileSelected");
  //myMovie = new Movie(this, "/Users/marco/Movies/drawing.mov");
  noLoop();
}

void fileSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
  } else {
    println("User selected " + selection.getAbsolutePath());
    myMovie = new Movie(this, selection.getAbsolutePath());
    myMovie.play();
  }
}

void draw() {
  if(myMovie != null)
  {
    image(myMovie, 0, 0, width, map(myMovie.height, 0, myMovie.width, 0,width));
    noLoop();
    currentFrame++;
  }
}

// Called every time a new frame is available to read
void movieEvent(Movie m) {
  m.read();
  fileName = "movie" + currentFrame + ".jpg";
  loop();
//  if (currentFrame >=0) {
  saveFrame(fileName);
//  }
  noLoop();
}

