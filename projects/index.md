---
layout: default
title: Projects
---

<style>
  .projects-header {
    padding-bottom: 1.8rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
  }

  .project-list {
    display: flex;
    flex-direction: column;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
  }

  .project-row {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: start;
    gap: 1rem;
    background: var(--bg);
    padding: 1.3rem 1.6rem;
    text-decoration: none;
    transition: background 0.2s;
  }
  .project-row:hover { background: var(--surface); }

  .project-row-title {
    font-family: var(--font-serif);
    font-size: 1.08rem;
    color: var(--text);
    margin-bottom: 0.25rem;
  }

  .project-row-desc {
    font-size: 0.82rem;
    color: var(--text-dim);
    line-height: 1.5;
    margin-bottom: 0.5rem;
  }

  .project-row-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
  }

  .project-row-tag {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 0.1em 0.45em;
    color: var(--muted);
  }

  .project-row-date {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-dim);
    white-space: nowrap;
    padding-top: 0.15rem;
  }
</style>

<div class="projects-header">
  <h1>Projects</h1>
</div>

<div class="project-list">
  {% assign sorted = site.projects | sort: 'date' | reverse %}
  {% for project in sorted %}
  <a class="project-row" href="{{ project.url | relative_url }}">
    <div>
      <div class="project-row-title">{{ project.title }}</div>
      <div class="project-row-desc">{{ project.description }}</div>
      {% if project.tags %}
      <div class="project-row-tags">
        {% for tag in project.tags %}
        <span class="project-row-tag">{{ tag }}</span>
        {% endfor %}
      </div>
      {% endif %}
    </div>
    {% if project.date %}
    <div class="project-row-date">{{ project.date | date: "%b %Y" }}</div>
    {% endif %}
  </a>
  {% endfor %}
</div>
