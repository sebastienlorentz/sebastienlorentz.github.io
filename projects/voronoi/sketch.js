new p5(function(p) {
  const W = 500, H = 340, N = 24;
  let seeds = [], cols = [];

  const PALETTE = [
    [180,210,190],[190,175,210],[210,190,160],
    [160,195,215],[215,185,170],[175,200,175],
    [200,180,200],[185,205,185],[210,175,185],
  ];

  p.setup = function() {
    p.createCanvas(W, H).parent('sketch');
    p.pixelDensity(1);
    p.noLoop();
    randomise();
    p.redraw();
  };

  p.mousePressed = function() {
    if (p.mouseX >= 0 && p.mouseX < W && p.mouseY >= 0 && p.mouseY < H) {
      randomise();
      p.redraw();
    }
  };

  p.draw = function() {
    p.loadPixels();
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        let minD = Infinity, secD = Infinity, nearest = 0;
        for (let i = 0; i < N; i++) {
          let d = (x - seeds[i].x) ** 2 + (y - seeds[i].y) ** 2;
          if (d < minD) { secD = minD; minD = d; nearest = i; }
          else if (d < secD) { secD = d; }
        }
        let onEdge = (Math.sqrt(secD) - Math.sqrt(minD)) < 2.5;
        let [r, g, b] = cols[nearest];
        let f = onEdge ? 0.45 : 1.0;
        let idx = 4 * (y * W + x);
        p.pixels[idx]     = r * f;
        p.pixels[idx + 1] = g * f;
        p.pixels[idx + 2] = b * f;
        p.pixels[idx + 3] = 255;
      }
    }
    p.updatePixels();
    seeds.forEach(s => {
      p.noStroke();
      p.fill(80, 80, 80, 180);
      p.circle(s.x, s.y, 4);
    });
  };

  function randomise() {
    seeds = Array.from({ length: N }, () =>
      p.createVector(p.random(W), p.random(H))
    );
    cols = seeds.map(() =>
      PALETTE[Math.floor(Math.random() * PALETTE.length)]
    );
  }
});
