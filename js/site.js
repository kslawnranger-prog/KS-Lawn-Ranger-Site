(function () {
  var menuBtn = document.getElementById("menuBtn");
  var menu = document.getElementById("mobileNav");
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.textContent = open ? "Close" : "Menu";
    });
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.classList.remove("is-open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.textContent = "Menu";
      });
    });
  }

  document.querySelectorAll("[data-ba]").forEach(function (block) {
    var range = block.querySelector('input[type="range"]');
    var after = block.querySelector(".ba-after");
    if (!range || !after) return;
    var sync = function () { after.style.width = range.value + "%"; };
    range.addEventListener("input", sync);
    sync();
  });

  var filters = document.querySelectorAll("[data-filter]");
  var figures = document.querySelectorAll("[data-cat]");
  filters.forEach(function (button) {
    button.addEventListener("click", function () {
      var cat = button.getAttribute("data-filter");
      filters.forEach(function (b) { b.setAttribute("aria-pressed", b === button ? "true" : "false"); });
      figures.forEach(function (fig) {
        var show = cat === "all" || fig.getAttribute("data-cat") === cat;
        fig.hidden = !show;
      });
    });
  });

  var dialog = document.getElementById("lightbox");
  var dialogImg = document.getElementById("lightboxImg");
  if (dialog && dialogImg) {
    document.querySelectorAll("[data-full]").forEach(function (button) {
      button.addEventListener("click", function () {
        dialogImg.src = button.getAttribute("data-full");
        dialogImg.alt = button.getAttribute("data-alt") || "";
        if (typeof dialog.showModal === "function") dialog.showModal();
      });
    });
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
  }

  var reviews = document.getElementById("google-reviews");
  if (reviews && "IntersectionObserver" in window) {
    var watcher = new IntersectionObserver(function (entries) {
      if (!entries.some(function (entry) { return entry.isIntersecting; })) return;
      watcher.disconnect();
      var script = document.createElement("script");
      script.src = "https://elfsightcdn.com/platform.js";
      script.async = true;
      document.body.appendChild(script);
      reviews.className = "elfsight-app-6adc10db-b8aa-48f7-aa11-0d204f5268b9";
      reviews.setAttribute("data-elfsight-app-lazy", "");
    }, { rootMargin: "300px" });
    watcher.observe(reviews);
  }

  document.querySelectorAll("form.quote-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      var errors = [];
      form.querySelectorAll(".is-invalid").forEach(function (el) { el.classList.remove("is-invalid"); });
      var name = form.querySelector('[name="name"]');
      var phone = form.querySelector('[name="phone"]');
      var email = form.querySelector('[name="email"]');
      var address = form.querySelector('[name="address"]');
      var message = form.querySelector('[name="message"]');
      var nameValue = (name.value || "").trim();
      if (nameValue.length < 2 || !/[A-Za-z]/.test(nameValue)) {
        errors.push("Enter your name.");
        name.closest(".field").classList.add("is-invalid");
      }
      var digits = (phone.value || "").replace(/\D/g, "");
      if (digits.length < 10) {
        errors.push("Enter a phone number with at least 10 digits.");
        phone.closest(".field").classList.add("is-invalid");
      }
      if (!email.checkValidity()) {
        errors.push("Enter a valid email address.");
        email.closest(".field").classList.add("is-invalid");
      }
      if ((address.value || "").trim().length < 5) {
        errors.push("Enter the property address.");
        address.closest(".field").classList.add("is-invalid");
      }
      if (!form.querySelector('input[name="property_type"]:checked')) {
        errors.push("Choose residential or commercial.");
      }
      if (!form.querySelector('input[name="services"]:checked')) {
        errors.push("Select at least one service.");
      }
      if (!form.querySelector('input[name="contact_method"]:checked')) {
        errors.push("Choose how you want to be contacted.");
      }
      var box = form.querySelector(".form-error");
      if (errors.length) {
        event.preventDefault();
        box.innerHTML = errors.map(function (item) { return "<div>" + item + "</div>"; }).join("");
        box.classList.add("is-on");
        box.focus();
        return;
      }
      box.classList.remove("is-on");
      name.value = nameValue;
      address.value = address.value.trim();
      if (message) message.value = message.value.trim();
    });
  });
})();
