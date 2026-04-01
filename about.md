---
layout: default
title: About
---

<style>
  .about-header {
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
  }

  .about-header h1 {
    font-size: 2.6rem;
    margin-bottom: 0.4rem;
  }

  .about-header .tagline {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .interest-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin: 1.5rem 0 2.5rem;
  }

  .interest-cell {
    background: var(--bg);
    padding: 1rem 1.2rem;
  }

  .interest-label {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 0.35rem;
  }

  .interest-value {
    font-family: var(--font-serif);
    font-size: 0.95rem;
    color: var(--text);
  }

  @media (max-width: 500px) {
    .interest-grid { grid-template-columns: 1fr; }
  }
</style>

<div class="about-header">
  <h1>About</h1>
  <p class="tagline">Applied mathematics · Durham University</p>
</div>

I'm a mathematics student with a focus on applied and computational methods.
This site collects small projects I build to understand something better —
usually at the boundary of theory and simulation.

## Interests

<div class="interest-grid">
  <div class="interest-cell">
    <div class="interest-label">Mathematics</div>
    <div class="interest-value">Mathematical biology, complex analysis, stochastic processes</div>
  </div>
  <div class="interest-cell">
    <div class="interest-label">Simulation</div>
    <div class="interest-value">Cellular automata, spatial models, reaction-diffusion systems</div>
  </div>
  <div class="interest-cell">
    <div class="interest-label">Visualisation</div>
    <div class="interest-value">p5.js, MATLAB, Python — making the abstract visible</div>
  </div>
  <div class="interest-cell">
    <div class="interest-label">Other</div>
    <div class="interest-value">Astrophotography, narrowband imaging, continuum subtraction</div>
  </div>
</div>

## Tools

I reach for **MATLAB** for numerical work, **Python** for scripting and data,
and **p5.js** for anything that benefits from an interactive canvas.
Mathematics on this site is rendered with MathJax — so equations like
$\nabla^2 u = f$ appear inline, and display-mode expressions like

$$\oint_\gamma f(z)\,dz = 2\pi i \sum_k \operatorname{Res}(f, z_k)$$

render properly.

## Contact

The best way to reach me is via the GitHub profile linked on each project page.
