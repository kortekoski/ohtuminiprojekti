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