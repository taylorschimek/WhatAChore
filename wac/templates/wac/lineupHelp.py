{% for person in people %}
<h6 class="text-primary text-center">{{ person.name }}</h6>
<ul class="list-group">

    {% for ass in assignments %}
        {% if ass.who == person %}
        <li class="list-group-item">
            <div>
              <p class="mb-0">{{ ass.what }}</p>
            </div>
            <div class="myBorder">
              <img src="{% static 'wac/styles/images/icons/utility/completedNO.png' %}" alt="">
              <!-- <p class="m-0 px-1">✓</p> -->
            </div>
        </li>
    {% endfor %}

</ul>
<hr />
{% endfor %}
