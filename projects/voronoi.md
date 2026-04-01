---
layout: project
title: "Voronoi Diagrams"
description: "Per-pixel Voronoi colouring with edge detection, built in p5.js."
date: 2026-04-01
language: JavaScript (p5.js)
github: https://github.com/gaba5/voronoi-p5
tags: [geometry, p5.js, visualisation]
uses_p5: true
---

## Overview

A Voronoi diagram partitions the plane into regions based on proximity to a
set of seed points. Each region $V_i$ consists of all points closer to seed
$\mathbf{s}_i$ than to any other seed:

$$V_i = \{ \mathbf{x} \in \mathbb{R}^2 : \|\mathbf{x} - \mathbf{s}_i\| \leq \|\mathbf{x} - \mathbf{s}_j\| \text{ for all } j \neq i \}$$

This implementation takes a brute-force per-pixel approach: for every pixel
$(x, y)$ on the canvas, we compute the Euclidean distance to each seed and
assign the pixel to the nearest one.

## Demo

<div class="demo-embed">
  <div class="demo-embed-label">Interactive — click to regenerate seeds</div>
  <div class="demo-embed-body">
    <div id="voronoi-sketch"></div>
  </div>
</div>

<script>
// p5.js sketch in instance mode so it doesn't pollute globals
new p5(function(p) {
  const W = 480, H = 360, N = 22;
  let seeds = [], cols = [], pixels;

  p.setup = function() {
    let cnv = p.createCanvas(W, H);
    cnv.parent('voronoi-sketch');
    p.pixelDensity(1);
    randomise();
    draw();
  };

  p.mousePressed = function() {
    if (p.mouseX >= 0 && p.mouseX < W && p.mouseY >= 0 && p.mouseY < H) {
      randomise(); draw();
    }
  };

  function randomise() {
    seeds = Array.from({length: N}, () => p.createVector(p.random(W), p.random(H)));
    // Warm palette — golds, slates, earthy tones
    const palette = [
      [200,169,110], [110,158,200], [160,130,170],
      [100,160,140], [190,130,100], [130,150,180],
      [170,155,120], [120,170,150], [155,125,165],
      [145,165,130], [195,155,125], [125,145,195],
    ];
    cols = seeds.map(() => palette[Math.floor(Math.random() * palette.length)]);
  }

  function draw() {
    p.loadPixels();
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        let minDist = Infinity, nearest = 0, secondDist = Infinity;
        for (let i = 0; i < N; i++) {
          let d = (x - seeds[i].x)**2 + (y - seeds[i].y)**2;
          if (d < minDist) { secondDist = minDist; minDist = d; nearest = i; }
          else if (d < secondDist) { secondDist = d; }
        }
        let idx = 4 * (y * W + x);
        // Edge detection: darken pixels near a boundary
        let edge = Math.sqrt(secondDist) - Math.sqrt(minDist) < 2.5;
        let [r, g, b] = cols[nearest];
        let dim = edge ? 0.25 : 1.0;
        p.pixels[idx]   = r * dim;
        p.pixels[idx+1] = g * dim;
        p.pixels[idx+2] = b * dim;
        p.pixels[idx+3] = 255;
      }
    }
    p.updatePixels();
    // Draw seed points
    p.noStroke();
    seeds.forEach(s => {
      p.fill(255, 255, 255, 180);
      p.circle(s.x, s.y, 5);
    });
  }
}, document.body);
</script>

## Implementation notes

**Brute-force complexity.** For $N$ seeds and a canvas of $W \times H$ pixels,
the naive approach runs in $O(N \cdot W \cdot H)$ time. For this sketch
($N = 22$, $480 \times 360$) that's around 3.8 million distance computations —
fast enough to run in under a second, but the approach doesn't scale well.
A [Fortune's algorithm](https://en.wikipedia.org/wiki/Fortune%27s_algorithm)
implementation would bring this to $O(N \log N)$.

**Edge detection.** Rather than tracing edges geometrically, we detect them
per-pixel: a pixel is on an edge if the gap between its nearest and
second-nearest seed distances is below a threshold $\varepsilon$:

$$\text{edge}(x,y) \iff d_2(x,y) - d_1(x,y) < \varepsilon$$

where $d_1, d_2$ are the nearest and second-nearest distances. The value
$\varepsilon = 2.5$ px gives clean single-pixel-wide edges.

**p5.js pixel density.** When drawing directly into the pixel buffer with
`loadPixels()`, it's essential to call `pixelDensity(1)` in `setup()` —
otherwise on retina/HiDPI displays the buffer is 4× larger than expected and
index arithmetic breaks silently.

## Source

The full annotated source is on GitHub. The core loop is about 25 lines.

```javascript
for (let y = 0; y < H; y++) {
  for (let x = 0; x < W; x++) {
    let minDist = Infinity, nearest = 0, secondDist = Infinity;
    for (let i = 0; i < seeds.length; i++) {
      let d = (x - seeds[i].x)**2 + (y - seeds[i].y)**2;
      if (d < minDist) { secondDist = minDist; minDist = d; nearest = i; }
      else if (d < secondDist) { secondDist = d; }
    }
    // colour pixel according to nearest seed ...
  }
}
```
