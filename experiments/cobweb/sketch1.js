let r = 0;
const n_iters = 50;
const n_points = 500;
const max_r=4;
const delta_r=0.02;

function setup() {
  pixelDensity(1);
  let size = document.body.offsetWidth;
  createCanvas(size, size);
}

function windowResized() {
  let size = document.body.offsetWidth;
  resizeCanvas(size, size);
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
  text('r = ' + r.toFixed(2), cx(0.5), 8);

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
  let x0 = 0.1;
  let y0 = x0;
  for (let i = 0; i < n_iters; i++) {
    let fx = r * x0 * (1 - x0);
    line(cx(x0), cy(y0), cx(x0), cy(fx));
    line(cx(x0), cy(fx), cx(fx), cy(fx));
    y0 = fx;
    x0 = fx;
  }

  // advance r
  r += delta_r;
  if (r > max_r) r = 0.1;
}
