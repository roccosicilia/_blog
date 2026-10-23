---
layout: page
title: Categorie
permalink: /categories/
nav_exclude: true
---

{% assign sorted_cats = site.categories | sort %}

<p class="category-index">
{%- for category in sorted_cats -%}
  <a class="post-category" href="#{{ category[0] | slugify }}">{{ category[0] }} ({{ category[1].size }})</a>
{%- endfor -%}
</p>

{% for category in sorted_cats %}
<h2 id="{{ category[0] | slugify }}">{{ category[0] }}</h2>
<ul class="category-posts">
  {%- for post in category[1] -%}
  <li>
    <span class="post-meta">{{ post.date | date: "%d-%m-%Y" }}</span>
    <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
  </li>
  {%- endfor -%}
</ul>
{% endfor %}