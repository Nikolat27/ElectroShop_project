const cmntReplyBtns = document.querySelectorAll('.cmnt--replybtn'),
replyFormTemplate = document.querySelector('[data-replyform-template]')

cmntReplyBtns.forEach(btn => {
    btn.addEventListener('click', addReplayForm)
})

function addReplayForm(e) {
    const body = document.getElementsByTagName('body')[0],
    replyform = replyFormTemplate.content.cloneNode(true).children[0]
    body.prepend(replyform)
}

function removeForm(elem) {
    elem.setAttribute('closing', '')
    elem.addEventListener('animationend', () => {
        elem.remove()
    }, {once: true})
}

function stopPropagation(e) {
    e.stopPropagation()
}