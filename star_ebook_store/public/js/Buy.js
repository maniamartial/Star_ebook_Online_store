document.addEventListener("DOMContentLoaded", function () {
  // Get a reference to the Buy button
  var buyButton = document.getElementById("buy-button");

  // Attach a click event listener
  buyButton.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default link behavior

    // Retrieve the ebook_name from the data attribute
    var ebookName = buyButton.getAttribute("data-ebook-name");

    // Make an AJAX request to the API endpoint
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json; charset=utf-8",
      "X-Frappe-CSRF-Token": "{{ csrf_token }}",
      Expect: "",
    };

    fetch("/api/method/star_ebook_store.www.api.create_ebook_order", {
      method: "POST",
      body: JSON.stringify({
        ebook_name: ebookName, // Use the retrieved value
      }),
      headers: headers,
    })
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          throw Error("Something went wrong");
        }
      })

      .then(function (orderData) {
        // Handle the response here if needed
        alert("Order created successfully. Order ID: ");
      })

      .catch(function (error) {
        // Handle errors here
        alert(error.message);
      });
  });
});
