// Makes every tag chip (.tag in page headers, .item-tag on cards) clickable,
// navigating to the combined tag collection at /tags.html?tag=<tag>.
// Uses event delegation so it covers chips added to any current or future page,
// and cancels the parent card link when a chip inside a card is clicked.
(function () {
  function go(tag) {
    window.location.href = "/tags.html?tag=" + encodeURIComponent(tag);
  }
  document.addEventListener("click", function (e) {
    var chip = e.target.closest(".tag, .item-tag");
    if (!chip) return;
    e.preventDefault();
    e.stopPropagation();
    // prefer an explicit data-tag (chips may carry extra text, e.g. a count)
    go((chip.dataset.tag || chip.textContent).trim());
  });
})();
