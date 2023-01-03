console.log("Sanity check!");

// Ajax request to the new /config/ endpoint
// Get the Stripe publishable key
fetch("/config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    console.log(data);
    const stripe = Stripe(data.publicKey);

    //Event handler
    let submitBtn = document.querySelector("#submitBtn");
    if (submitBtn !== null) {
      submitBtn.addEventListener("click", () => {
        console.log("Button clicked");
        // Get Checkout Session ID
        fetch("/create-checkout-session/")
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            console.log(data);
            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .then((res) => {
            console.log(res);
          });
      });
    }
  });