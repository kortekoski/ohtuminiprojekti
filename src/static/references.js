// Copy BibTeX content to clipboard
const copyToClipboard = (bibtexContent) => {
  if (bibtexContent.length === 0) {
    window.lastCopiedBibtex = '';
    window.alert('No entries to copy!');
  } else {
    window.lastCopiedBibtex = bibtexContent;
    navigator.clipboard.writeText(bibtexContent).then(() => {
      alert('BibTeX copied to clipboard!');
    }).catch(err => {
      alert('Failed to copy: ' + err);
    });
  }
};

// Copy selected references to clipboard
const copy_selected = () => {
  const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
  const bibtexData = Array.from(checkedBoxes).map(checked => checked.getAttribute('bibtex-data'));
  copyToClipboard(bibtexData.join('\n'));
};

// Download selected references as BibTeX file
const download_selected = () => {
  const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
  const checkedRefIds = Array.from(checkedBoxes).map(checked => checked.getAttribute('ref-id'));

  const url = new URL("/download_selected_bibtex", window.location.origin);
  
  for (const refId of checkedRefIds) {
    url.searchParams.append('ref_id', refId);
  }

  window.location.href = url;
};
