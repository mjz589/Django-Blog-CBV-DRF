{% extends "mail_templated/base.tpl" %}

{% block subject %}
Rest Password
{% endblock %}

{% block html %}
<a href="http://127.0.0.1:8000/accounts/api/v1/reset-password-confirm/{{token}}">Rest your password with this url</a>
{% endblock %}