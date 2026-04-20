let r = 3;
let x0 = 0;
const n_iters = 50;
const n_points = 500;
const max_x=1;
const delta_x=0.005;

function setup() {
  createCanvas(400, 400)
}

function draw() {
  background(255);

  let m = 50;
  let w = width - 2 * m;
  let h = height - 2 * m;

  function cx(x) { return m + x * w; }
  function cy(y) { return m + (1 - y) * h; }

  // grid
  stroke(220);
  strokeWeight(1);
  for (let i = 0; i <= 5; i++) {
    let t = i / 5;
    line(cx(t), cy(0), cx(t), cy(1));
    line(cx(0), cy(t), cx(1), cy(t));
  }

  // axes
  stroke(0);
  strokeWeight(1.5);
  line(cx(0), cy(0), cx(1), cy(0));
  line(cx(0), cy(0), cx(0), cy(1));

  // tick labels
  noStroke();
  fill(0);
  textSize(10);
  textAlign(CENTER, TOP);
  for (let i = 0; i <= 5; i++) {
    let t = i / 5;
    text(t.toFixed(1), cx(t), cy(0) + 4);
  }
  textAlign(RIGHT, CENTER);
  for (let i = 0; i <= 5; i++) {
    let t = i / 5;
    text(t.toFixed(1), cx(0) - 4, cy(t));
  }

  // axis labels
  textAlign(CENTER);
  textSize(13);
  text('x', cx(0.5), height - 5);
  push();
  translate(12, cy(0.5));
  rotate(-HALF_PI);
  text('y', 0, 0);
  pop();

  // title
  textAlign(CENTER, TOP);
  text('x0 = ' + x0.toFixed(2), cx(0.5), 8);

  // f(x) = r*x*(1-x)
  stroke(0);
  strokeWeight(1.5);
  noFill();
  beginShape();
  for (let i = 0; i <= n_points; i++) {
    let x = i / n_points;
    let y = r * x * (1 - x);
    vertex(cx(x), cy(y));
  }
  endShape();

  // y = x diagonal
  line(cx(0), cy(0), cx(1), cy(1));

// cobweb
  stroke(255, 0, 0);
  strokeWeight(1);
  let x = x0;  // local copy — do not modify x0
  let y0 = x0;
  for (let i = 0; i < n_iters; i++) {
    let fx = r * x * (1 - x);
    line(cx(x), cy(y0), cx(x), cy(fx));
    line(cx(x), cy(fx), cx(fx), cy(fx));
    y0 = fx;
    x = fx;
  }

  // advance x0 for next frame
  x0 += delta_x;
  if (x0 > max_x) x0 = 0.1;
}