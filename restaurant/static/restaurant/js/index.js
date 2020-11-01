function findFormElement(prefix, field) {
    return $(`#id_${prefix}-${field}`)
}

class CreateDishForm {
    constructor (prefix, action) {
        this.prefix = prefix;
        this.action = action;

        this.name = findFormElement(prefix, "name");
        this.nutritional_value = findFormElement(prefix, "nutritional_value");
        this.price = findFormElement(prefix, "price_0");
        this.price_currency = findFormElement(prefix, "price_1");
        this.image = findFormElement(prefix, "image");
        this.category = findFormElement(prefix, "category");
        this.allergens = findFormElement(prefix, "allergens");

        this.api_key = findFormElement(prefix, "api_key");

        this.errorMessage = findFormElement(prefix, "errorMessage");

        this.submitButton = findFormElement(prefix, "submit");
        this.submitButton.on("click", () => this.submit());
    }

    get data() {
        let data = {
            "name": this.name.val(),
            "nutritional_value": this.nutritional_value.val(),
            "price": this.price.val(),
            "price_currency": this.price_currency.val(),
            "category": this.category.val(),
            "allergens": this.allergens.val()
        };
        return data;
    }

    get formData() {
        let fd = new FormData();
        for (const [k, v] of Object.entries(this.data)) {
            fd.append(k, v);
        }
        let image = this.image[0].files[0];
        if (image !== undefined) {
            fd.append("image", image);
        }
        return fd;
    }

    submit () {
        for (const e of this.formData.entries()) {console.log(e)}
        let createDishUrl = this.action;
        let apiKey = this.api_key.val();
        $.ajax({
            url: createDishUrl,
            type: "POST",
            data: this.formData,
            contentType: false,
            processData: false,
            headers: {
                "Authorization": `Bearer ${apiKey}`
            }
        })
            .done((res) => {
                alert(`Created dish with id ${res.id}`);
                location.reload();
            })
            .fail((err) => {
                err = JSON.stringify(err);
                this.errorMessage.text(err);
            });
    }
}
