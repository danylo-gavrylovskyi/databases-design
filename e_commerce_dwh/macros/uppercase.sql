{% macro uppercase(column_name) %}
UPPER({{ column_name }})
{% endmacro %}
