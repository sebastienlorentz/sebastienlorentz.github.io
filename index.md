---
layout: default
title: Home
---

<style>
  /* Homepage-specific styles */
  .hero {
    padding: 3rem 0 3.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
  }

  .hero h1 {
    font-size: 3rem;
    line-height: 1.1;
    margin-bottom: 1rem;
  }

  .hero h1 em {
    font-style: italic;
    color: var(--accent);
  }

  .hero-lead {
    font-size: 1.05rem;
    color: var(--text-dim);
    max-width: 520px;
    line-height: 1.7;
    margin-bottom: 0;
  }

  /* Section label */
  .section-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 1.5rem;
  }

  /* Project card grid */
  .project-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1.5rem;
  }

  .project-card {
    background: var(--bg);
    padding: 1.4rem 1.6rem;
    text-decoration: none;
    display: block;
    transition: background 0.2s;
  }
  .project-card:hover { background: var(--surface); }

  .card-title {
    font-family: var(--font-serif);
    font-size: 1.05rem;
    color: var(--text);
    margin-bottom: 0.3rem;
  }

  .card-desc {
    font-size: 0.82rem;
    color: var(--text-dim);
    line-height: 1.5;
    margin-bottom: 0.7rem;
  }

  .card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
  }

  .card-tag {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 0.1em 0.45em;
    color: var(--muted);
  }

  .all-projects-link {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }
  .all-projects-link:hover { color: var(--accent); }
  .all-projects-link::after { content: ' →'; }

  @media (max-width: 540px) {
    .project-grid { grid-template-columns: 1fr; }
    .hero h1 { font-size: 2.2rem; }
  }
</style>

<div class="hero">
  <h1>Maths,<br/><em>in practice.</em></h1>
  <p class="hero-lead">
    A collection of small experiments at the intersection of mathematics,
    simulation, and code — built to understand things by making them.
  </p>
</div>

<p class="section-label">Recent projects</p>

<div class="project-grid">
  {% assign recent = site.projects | sort: 'date' | reverse | limit: 4 %}
  {% for project in recent %}
  <a class="project-card" href="{{ project.url | relative_url }}">
    <div class="card-title">{{ project.title }}</div>
    <div class="card-desc">{{ project.description }}</div>
    {% if project.tags %}
    <div class="card-tags">
      {% for tag in project.tags %}
      <span class="card-tag">{{ tag }}</span>
      {% endfor %}
    </div>
    {% endif %}
  </a>
  {% endfor %}
</div>

<a class="all-projects-link" href="{{ '/projects/' | relative_url }}">All projects</a>
