console.log("JS loaded!");

document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_category');
    console.log("DOM Loaded, categorySelect:", categorySelect);

    function fetchAttributes(categoryId) {
        console.log("Fetching attributes for category:", categoryId);
        fetch(`/admin/get-category-attributes/${categoryId}/`)
            .then(response => {
                console.log("Response received:", response);
                return response.json();
            })
            .then(data => {
                console.log("Attribute data:", data);
                const container = document.getElementById('attribute-container');
                container.innerHTML = '';

                data.forEach(attr => {
                    const wrapper = document.createElement('div');
                    wrapper.style.marginBottom = '10px';

                    const label = document.createElement('label');
                    label.htmlFor = `id_attr_${attr.id}`;
                    label.textContent = attr.name;
                    label.style.display = 'block';

                    const field = document.createElement('input');
                    field.name = `attr_${attr.id}`;
                    field.id = `id_attr_${attr.id}`;
                    field.placeholder = attr.name;
                    field.required = attr.required;
                    field.classList.add('vTextField');

                    wrapper.appendChild(label);
                    wrapper.appendChild(field);
                    container.appendChild(wrapper);
                });
            })
            .catch(err => console.error("Error fetching attributes:", err));
    }

    if (categorySelect) {
        if (categorySelect.value) {
            fetchAttributes(categorySelect.value);
        }

        categorySelect.addEventListener('change', function () {
            if (this.value) {
                fetchAttributes(this.value);
            }
        });
    }
});
