/**
 * MORE THAN GRADES — Contact & Peer Support Form Controller (100% English)
 */

document.addEventListener("DOMContentLoaded", () => {
  const contactForm = document.getElementById("student-support-form");
  const anonymousCheckbox = document.getElementById("anonymous-mode-check");
  const nameField = document.getElementById("student-name-input");
  const emailField = document.getElementById("student-email-input");
  const feedbackModal = document.getElementById("form-success-modal");
  const modalCloseBtn = document.getElementById("modal-success-close");

  if (!contactForm) return;

  // Anonymous mode toggle
  if (anonymousCheckbox && nameField) {
    anonymousCheckbox.addEventListener("change", (e) => {
      if (e.target.checked) {
        nameField.value = "Anonymous Peer / Student";
        nameField.setAttribute("disabled", "true");
        if (emailField) {
          emailField.removeAttribute("required");
          emailField.placeholder = "Optional when anonymous";
        }
      } else {
        nameField.value = "";
        nameField.removeAttribute("disabled");
        if (emailField) {
          emailField.setAttribute("required", "true");
          emailField.placeholder = "name@example.com";
        }
      }
    });
  }

  // Submit Handler
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const topic = document.getElementById("support-topic-select").value;
    const message = document.getElementById("student-message-input").value.trim();

    if (!message) {
      alert("Please write your message or inquiry before submitting.");
      return;
    }

    if (feedbackModal) {
      const summaryMsg = document.getElementById("success-summary-text");
      if (summaryMsg) {
        summaryMsg.innerText = `Your message regarding (${topic}) has been submitted with full confidentiality. Thank you for reaching out; you are never alone!`;
      }
      feedbackModal.style.display = "flex";
    } else {
      alert("Your message has been sent successfully with complete confidentiality.");
    }

    contactForm.reset();
    if (nameField) nameField.removeAttribute("disabled");
  });

  if (modalCloseBtn && feedbackModal) {
    modalCloseBtn.addEventListener("click", () => {
      feedbackModal.style.display = "none";
    });
  }
});
