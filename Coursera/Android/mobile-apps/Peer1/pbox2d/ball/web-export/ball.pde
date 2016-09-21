PBox2D box2d;
 
void setup() {
  box2d = new PBox2D(this);
  box2d.createWorld();
  box2d.setGravity(0, -10);
  BodyDef bd = new BodyDef();
  Vec2 center = new Vec2(width/2,height/2);
  Vec2 center = box2d.coordPixelsToWorld(width/2,height/2);
  bd.position.set(center);
  bd.linearDamping = 0.8;
  bd.angularDamping = 0.9;
  Body body = box2d.createBody(bd);
  bd.setLinearVelocity(new Vec2(0,3));
  bd.setAngularVelocity(1.2);
  
  CircleShape cs = new CircleShape();
  float radius = 10;
  cs.m_radius = box2d.scalarPixelsToWorld(10);;
  FixtureDef fd = new FixtureDef();
  fd.shape = cs;
  fd.density = 1;
  fd.friction = 0.1;
  fd.restitution = 0.3;
 
  body.createFixture(fd);
}


class Box  {
  float x,y;
  float w,h;
 
  Box(float x_, float y_) {
    x = x_;
    y = y_;
    w = 16;
    h = 16;
  }
 
  void display() {
    fill(175);
    stroke(0);
    rectMode(CENTER);
    rect(x,y,w,h);
  }
}


Box box = new Box(60,70);

