
ArrayList lines = new ArrayList();
int [] mouse_lines = new int[4];
String coordinates;
int [] ml = new int[4];
  
void setup() {
  int screen_width = 512;
  int screen_height = 512;
  int screen_size = screen_width * screen_height;
  size(screen_width,screen_height);/* setup the size */
  background(255);
  //int [] s_p = new int(screen_size);
  

}


void draw() {
  background(255);
  stroke(0);
  strokeWeight(6);
  String temp = "8 67 5 309";
  //for (int i =0; i < lines.size(); i++) {
    //int[] ml = int(split(lines.get(i), ','));
    ml = int(split(temp, ','));
  //  println(int(split(lines.get(i), ',')));
  //  println(lines.get(i));
    println(temp); 
    println(ml);
    //println(ml[1]);
    //line(ml[0], ml[1], ml[2], ml[3]);
    //line(0, 0, 255, 255);
  //}
  //line(0, 0, 255, 255);
  
}

void mousePressed() {
  mouse_lines[0] = mouseX;
  mouse_lines[1] = mouseY;
}

void mouseReleased() {
  mouse_lines[2] = mouseX;
  mouse_lines[3] = mouseY;
  //println(mouse_lines);
  //coordinates = join(nf(mouse_lines, 0), ", ");
  lines.add(mouse_lines);
}
