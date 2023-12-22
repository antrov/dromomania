import os
import imagehash
from PIL import Image
from jinja2 import Template
import functools

# Ścieżka do folderu z obrazami
folder_path = './samples'

# Lista przechowująca hashe obrazów
image_hashes = []

# Tworzenie listy obrazów i ich hashy
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        image_path = os.path.join(folder_path, filename)
        img = Image.open(image_path)
        cmp_hash = imagehash.phash(img)
        image_hashes.append((image_path, cmp_hash))

# Maksymalna różnica między hashami
max_hash_difference = 13

# Grupowanie obrazów kady z kazdym
image_families = []
for base_idx, (_, base_hash) in enumerate(image_hashes):
    current_family = []
    for cmp_idx, (cmp_image, cmp_hash) in enumerate(image_hashes):
        if cmp_idx == base_idx: continue
        if abs(base_hash - cmp_hash) <= max_hash_difference:
            current_family.append((cmp_image, abs(base_hash - cmp_hash)))
    image_families.append(current_family)

template = Template('''
<!DOCTYPE html>
<html>
<head>
  <title>Images Families</title>
  <style>
    table {
      border-collapse: collapse;
    }
    table, th, td {
      border: 1px solid black;
      padding: 8px;
    }
  </style>
</head>
<body>
  <h1>Images Families</h1>
  <caption>Diff each-to-each hash</caption>
  <table>
    <tr>
      <th>Group</th>
      <th>Images</th>
    </tr>
    {% for image_hash in image_hashes %}
      <tr>
        <td>
            <img src="{{ image_hash[0] }}" style="max-height: 200px; max-width: 200px;">
        </td>
        <td>
            {% for image_family in image_families[loop.index-1] %}
              <figure style="display: inline-block;">
                <img src="{{ image_family[0] }}" style="max-height: 200px; max-width: 200px;">
                <figcaption>Diff: <code>{{ image_family[1] }}</code></figcaption>
              </figure>
            {% endfor %}
        </td>
      </tr>
    {% endfor %}
  </table>
</body>
</html>
''')

rendered_template = template.render(image_families=image_families,image_hashes=image_hashes)

# Zapisanie strony do pliku HTML
with open('families.html', 'w') as file:
    file.write(rendered_template)

# Grupowanie obrazów na podstawie różnicy hashów
image_groups = []
while len(image_hashes) > 0:
    current_image, base_hash = image_hashes.pop(0)
    current_group = [(current_image, base_hash)]

    to_remove = []
    for cmp_idx, (cmp_image, cmp_hash) in enumerate(image_hashes):
        if abs(base_hash - cmp_hash) <= max_hash_difference:
            current_group.append((cmp_image, cmp_hash))
            to_remove.append(cmp_idx)

    image_groups.append(current_group)
    image_hashes = [image for i, image in enumerate(image_hashes) if i not in to_remove]

# Generowanie strony internetowej
template = Template('''
<!DOCTYPE html>
<html>
<head>
  <title>Grouped Images</title>
  <style>
    table {
      border-collapse: collapse;
    }
    table, th, td {
      border: 1px solid black;
      padding: 8px;
    }
  </style>
</head>
<body>
  <h1>Grouped Images</h1>
  <table>
    <tr>
      <th>Group</th>
      <th>Images</th>
    </tr>
    {% for group in image_groups %}
      {% if group|length > 0 %}
      <tr>
        <td>
            {{ loop.index }}
        </td>
        <td>
          <ul>
            {% for image_with_hash in group %}
            <li>
              <img src="{{ image_with_hash[0] }}" style="max-height: 200px; max-width: 200px;">
              {{ image_with_hash[0] }}
            </li>
            {% endfor %}
          </ul>
        </td>
      </tr>
      {% endif %}
    {% endfor %}
  </table>
</body>
</html>
''')

rendered_template = template.render(image_groups=image_groups)

# Zapisanie strony do pliku HTML
with open('grouped_images.html', 'w') as file:
    file.write(rendered_template)

