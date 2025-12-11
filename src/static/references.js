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

const getCheckedRefIds = () => {
  const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
  const checkedRefIds = Array.from(checkedBoxes).map(checked => checked.getAttribute('ref-id'));

  return checkedRefIds;
}

const getCheckedCitationKeys = () => {
  const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
  const checkedCitationKeys = Array.from(checkedBoxes).map(checked => checked.getAttribute('ref-citation-key'));

  return checkedCitationKeys;
}

// Download selected references as BibTeX file
const download_selected = () => {
  const checkedRefIds = getCheckedRefIds();

  const url = new URL("/download_selected_bibtex", window.location.origin);
  
  for (const refId of checkedRefIds) {
    url.searchParams.append('ref_id', refId);
  }

  window.location.href = url;
};

// Gets citation keys from checked references, creates a form with them as input and submits it
const delete_selected = () => {
  const checkedCitationKeys = getCheckedCitationKeys();
  if (checkedCitationKeys.length === 0) {
    alert('No references selected for deletion!');
    return;
  }

  if (!confirm(`Delete ${checkedCitationKeys.length} selected reference(s)?`)) {
    return;
  }

  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/delete_selected_references';

  for (const citation_key of checkedCitationKeys) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'citation_key';
    input.value = citation_key;
    form.appendChild(input);
  }

  document.body.appendChild(form);
  form.submit();
};

