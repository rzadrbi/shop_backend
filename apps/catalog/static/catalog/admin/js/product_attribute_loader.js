document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_category');

    function fetchAttributes(categoryId) {
        // درخواست AJAX برای گرفتن attributeهای مربوط به category
        fetch(`/admin/get-category-attributes/${categoryId}/`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('attribute-container');
                container.innerHTML = ''; // پاک کردن فیلدهای قبلی

                data.forEach(attr => {
                    const field = document.createElement('input');
                    field.name = `attr_${attr.id}`;
                    field.id = `id_attr_${attr.id}`;
                    field.placeholder = attr.name;
                    field.required = attr.required;
                    field.classList.add('vTextField');  // برای استایل admin
                    container.appendChild(field);
                });
            });
    }

    if (categorySelect) {
        // ابتدا اگر انتخاب شده بود اجرا کن
        if (categorySelect.value) {
            fetchAttributes(categorySelect.value);
        }

        categorySelect.addEventListener('change', function () {
            if (this.value) {
                fetchAttributes(this.value);
            }
        });

        // ایجاد container برای فیلدهای attribute
        const formRow = document.querySelector('#id_category').closest('.form-row');
        const attrContainer = document.createElement('div');
        attrContainer.id = 'attribute-container';
        formRow.parentNode.insertBefore(attrContainer, formRow.nextSibling);
    }
});
