/**
 * DigiHust Lead Management System — Frontend Application Logic
 */

(function () {
  "use strict";

  // ── DOM References ──────────────────────────────────────────
  const form            = document.getElementById("leadForm");
  const submitBtn       = document.getElementById("submitBtn");
  const successPanel    = document.getElementById("successMessage");
  const leadIdDisplay   = document.getElementById("leadIdDisplay");
  const newLeadBtn      = document.getElementById("newLeadBtn");
  const errorBanner     = document.getElementById("errorBanner");
  const errorBannerText = document.getElementById("errorBannerText");
  const errorBannerClose= document.getElementById("errorBannerClose");
  const messageInput    = document.getElementById("message");
  const messageCount    = document.getElementById("message-count");

  const serviceSelect   = document.getElementById("service");
  const budgetSelect    = document.getElementById("budget");
  const servicePills    = document.getElementById("service-pills");
  const budgetPills     = document.getElementById("budget-pills");

  // ── Populate Dropdowns & Pill Selectors ──────────────────────
  function populateDropdownsAndPills() {
    // Services
    APP_CONFIG.SERVICES.forEach(function (svc) {
      // Option
      const opt = document.createElement("option");
      opt.value = svc;
      opt.textContent = svc;
      serviceSelect.appendChild(opt);

      // Pill
      const pill = document.createElement("button");
      pill.type = "button";
      pill.className = "pill-option";
      pill.textContent = svc;
      pill.addEventListener("click", function () {
        serviceSelect.value = svc;
        updatePillSelection(servicePills, pill);
        validateField("service");
      });
      servicePills.appendChild(pill);
    });

    // Budgets
    APP_CONFIG.BUDGETS.forEach(function (b) {
      // Option
      const opt = document.createElement("option");
      opt.value = b;
      opt.textContent = b;
      budgetSelect.appendChild(opt);

      // Pill
      const pill = document.createElement("button");
      pill.type = "button";
      pill.className = "pill-option";
      pill.textContent = b;
      pill.addEventListener("click", function () {
        budgetSelect.value = b;
        updatePillSelection(budgetPills, pill);
        validateField("budget");
      });
      budgetPills.appendChild(pill);
    });

    // Sync select dropdown change to pills
    serviceSelect.addEventListener("change", function () {
      syncSelectToPills(serviceSelect, servicePills);
    });
    budgetSelect.addEventListener("change", function () {
      syncSelectToPills(budgetSelect, budgetPills);
    });
  }

  function updatePillSelection(container, activePill) {
    container.querySelectorAll(".pill-option").forEach(function (p) {
      p.classList.remove("active");
    });
    if (activePill) {
      activePill.classList.add("active");
    }
  }

  function syncSelectToPills(selectEl, container) {
    const val = selectEl.value;
    container.querySelectorAll(".pill-option").forEach(function (p) {
      if (p.textContent === val) {
        p.classList.add("active");
      } else {
        p.classList.remove("active");
      }
    });
  }

  // ── Sanitization ────────────────────────────────────────────
  function sanitizeHTML(str) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  function cleanString(str) {
    return (str || "").trim().replace(/\s+/g, " ");
  }

  // ── Validation Logic ────────────────────────────────────────
  var validators = {
    name: function (value) {
      var v = cleanString(value);
      if (!v) return "Full name is required.";
      if (v.length < APP_CONFIG.VALIDATION.NAME_MIN_LENGTH)
        return "Name must be at least " + APP_CONFIG.VALIDATION.NAME_MIN_LENGTH + " characters.";
      if (v.length > APP_CONFIG.VALIDATION.NAME_MAX_LENGTH)
        return "Name must be under " + APP_CONFIG.VALIDATION.NAME_MAX_LENGTH + " characters.";
      return "";
    },

    email: function (value) {
      var v = cleanString(value);
      if (!v) return "Email address is required.";
      if (!APP_CONFIG.VALIDATION.EMAIL_REGEX.test(v))
        return "Please enter a valid email address.";
      return "";
    },

    phone: function (value) {
      var v = cleanString(value);
      if (!v) return "Phone number is required.";
      if (!APP_CONFIG.VALIDATION.PHONE_REGEX.test(v))
        return "Please enter a valid phone number (e.g. 03123456789).";
      return "";
    },

    company: function (value) {
      var v = cleanString(value);
      if (!v) return "Company name is required.";
      if (v.length > APP_CONFIG.VALIDATION.COMPANY_MAX_LENGTH)
        return "Company name must be under " + APP_CONFIG.VALIDATION.COMPANY_MAX_LENGTH + " characters.";
      return "";
    },

    service: function (value) {
      if (!value) return "Please select a service.";
      return "";
    },

    budget: function (value) {
      if (!value) return "Please select a budget range.";
      return "";
    },

    message: function (value) {
      var v = cleanString(value);
      if (!v) return "Please describe your project.";
      if (v.length > APP_CONFIG.VALIDATION.MESSAGE_MAX_LENGTH)
        return "Message must be under " + APP_CONFIG.VALIDATION.MESSAGE_MAX_LENGTH + " characters.";
      return "";
    }
  };

  function validateField(fieldId) {
    var input = document.getElementById(fieldId);
    var errorSpan = document.getElementById("error-" + fieldId);
    if (!input || !errorSpan) return true;

    var value = input.value;
    var error = validators[fieldId](value);

    if (error) {
      input.classList.add("invalid");
      input.classList.remove("valid");
      errorSpan.textContent = error;
      return false;
    } else {
      input.classList.remove("invalid");
      input.classList.add("valid");
      errorSpan.textContent = "";
      return true;
    }
  }

  function validateAll() {
    var fields = ["name", "email", "phone", "company", "service", "budget", "message"];
    var allValid = true;
    fields.forEach(function (f) {
      if (!validateField(f)) allValid = false;
    });
    return allValid;
  }

  // Real-time validation listeners
  ["name", "email", "phone", "company", "service", "budget", "message"].forEach(function (fieldId) {
    var input = document.getElementById(fieldId);
    if (!input) return;
    input.addEventListener("blur", function () {
      validateField(fieldId);
    });
    input.addEventListener("input", function () {
      if (input.classList.contains("invalid")) {
        validateField(fieldId);
      }
    });
  });

  // Character counter
  if (messageInput && messageCount) {
    messageInput.addEventListener("input", function () {
      var len = messageInput.value.length;
      messageCount.textContent = len + " / " + APP_CONFIG.VALIDATION.MESSAGE_MAX_LENGTH;
    });
  }

  // ── Error Banner ────────────────────────────────────────────
  function showError(message) {
    errorBannerText.textContent = message;
    errorBanner.hidden = false;
    // Scroll to error banner if not visible
    errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  if (errorBannerClose) {
    errorBannerClose.addEventListener("click", function () {
      errorBanner.hidden = true;
    });
  }

  // ── Form Submission ─────────────────────────────────────────
  function setLoading(loading) {
    if (loading) {
      submitBtn.classList.add("loading");
      submitBtn.disabled = true;
    } else {
      submitBtn.classList.remove("loading");
      submitBtn.disabled = false;
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!validateAll()) {
      var firstError = form.querySelector(".invalid");
      if (firstError) firstError.focus();
      return;
    }

    var payload = {
      name:    cleanString(document.getElementById("name").value),
      email:   cleanString(document.getElementById("email").value).toLowerCase(),
      phone:   cleanString(document.getElementById("phone").value),
      company: cleanString(document.getElementById("company").value),
      service: document.getElementById("service").value,
      budget:  document.getElementById("budget").value,
      message: cleanString(document.getElementById("message").value)
    };

    setLoading(true);
    errorBanner.hidden = true;

    var controller = new AbortController();
    var timeoutId = setTimeout(function () {
      controller.abort();
    }, APP_CONFIG.SUBMIT_TIMEOUT_MS);

    fetch(APP_CONFIG.WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal
    })
    .then(function (response) {
      clearTimeout(timeoutId);
      return response.json().then(function (data) {
        if (!response.ok) {
          // If n8n returned validation errors array or message
          if (data && data.errors && Array.isArray(data.errors)) {
            throw new Error(data.errors.join(" | "));
          }
          throw new Error((data && data.message) || ("Server returned " + response.status));
        }
        return data;
      }).catch(function (parseErr) {
        if (parseErr.message) throw parseErr;
        throw new Error("Unable to connect to lead service. Please try again.");
      });
    })
    .then(function (data) {
      setLoading(false);

      if (data && data.success === false) {
        var msg = data.message || "Lead processing failed.";
        if (data.errors && Array.isArray(data.errors)) {
          msg = data.errors.join(" | ");
        }
        showError(msg);
        return;
      }

      // Success or Duplicate Handled
      form.hidden = true;
      if (data && data.lead_id) {
        leadIdDisplay.textContent = sanitizeHTML(data.lead_id);
      } else {
        leadIdDisplay.textContent = "Submitted";
      }

      successPanel.hidden = false;
      successPanel.scrollIntoView({ behavior: "smooth", block: "center" });
    })
    .catch(function (err) {
      setLoading(false);
      if (err.name === "AbortError") {
        showError("Request timed out. Please check your connection and try again.");
      } else {
        showError(err.message || "Failed to submit inquiry. Please try again.");
      }
    });
  });

  // ── New Lead Reset Button ───────────────────────────────────
  if (newLeadBtn) {
    newLeadBtn.addEventListener("click", function () {
      successPanel.hidden = true;
      form.hidden = false;
      form.reset();

      // Clear pills
      servicePills.querySelectorAll(".pill-option").forEach(p => p.classList.remove("active"));
      budgetPills.querySelectorAll(".pill-option").forEach(p => p.classList.remove("active"));

      // Clear validation states
      form.querySelectorAll(".form-input").forEach(function (input) {
        input.classList.remove("valid", "invalid");
      });
      form.querySelectorAll(".form-error").forEach(function (span) {
        span.textContent = "";
      });
      if (messageCount) {
        messageCount.textContent = "0 / " + APP_CONFIG.VALIDATION.MESSAGE_MAX_LENGTH;
      }
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  // ── Initialize ──────────────────────────────────────────────
  populateDropdownsAndPills();
})();
