---
layout: page
title: Hello World!
---
{% include JB/setup %}

I am in the process on moving my content over here.  Still waiting for the dust to settle.

In the meantime, here are some really old posts:

<ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
