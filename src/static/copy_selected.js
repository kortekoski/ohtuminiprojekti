const copy_selected = () => {
    const checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked')

    const bibtexData = Array.from(checkedBoxes).map(checked => checked.getAttribute('bibtex-data'))

    copyToClipboard(bibtexData.join('\n'))
}