document.addEventListener("click", (e) => {
  const editBtn = e.target.closest(".image-card__action--edit");
  if (editBtn) {
    const group = editBtn.closest(".image-card__name-group");
    group.classList.add("image-card__name-group--editing");
    const input = group.querySelector(".image-card__input");
    input.focus();
    const val = input.value;
    input.value = "";
    input.value = val;
    return;
  }

  const copyBtn = e.target.closest(".image-card__action--copy");
  if (copyBtn && copyBtn.dataset.url) {
    navigator.clipboard.writeText(copyBtn.dataset.url);
  }
});

function saveEdit(e) {
  const form = e.target.closest("form");
  const saveButton = form.querySelector('input[name="_save"]');

  form.requestSubmit(saveButton);
}

document.addEventListener("focusout", (e) => {
  if (!e.target.matches(".image-card__input")) return;
  const group = e.target.closest(".image-card__name-group");
  group.classList.remove("image-card__name-group--editing");
  saveEdit(e);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.target.matches(".image-card__input")) {
    e.preventDefault();
    saveEdit(e);
  }
});
