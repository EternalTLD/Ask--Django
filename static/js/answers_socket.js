const questionId = JSON.parse(document.getElementById('questionId').textContent);
const answersSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/questions/' + questionId + '/'
);


answersSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const answersList = document.getElementById('answers-list');
    const answer = answerBuilder(data);
    answersList.insertAdjacentElement('afterbegin', answer);
};


function answerBuilder(data) {
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body border rounded';

    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'd-flex flex-start align-items-center';

    const avatar = document.createElement('img');
    avatar.className = 'rounded-circle shadow-1-strong me-3';
    avatar.src = data['message']['profile_image'];
    avatar.alt = 'avatar';
    avatar.width = 60;
    avatar.height = 60;

    const authorInfo = document.createElement('div');

    const authorName = document.createElement('h6');
    authorName.className = 'fw-bold text-primary mb-1';
    const authorLink = document.createElement('a');
    authorLink.href = data['message']['author_url'];
    authorLink.textContent = data['message']['author'];
    authorName.appendChild(authorLink);

    const publishedDate = document.createElement('p');
    publishedDate.className = 'text-muted small mb-0';
    publishedDate.textContent = 'Опубликовано - ' + data['message']['date_published'];

    authorInfo.appendChild(authorName);
    authorInfo.appendChild(publishedDate);

    contentWrapper.appendChild(avatar);
    contentWrapper.appendChild(authorInfo);

    const messageContent = document.createElement('p');
    messageContent.className = 'mt-3 mb-4 pb-2';
    messageContent.textContent = data['message']['content'];

    const voteContainer = document.createElement('div');
    const votes = votesBuilder(data);
    voteContainer.appendChild(votes)

    cardBody.appendChild(contentWrapper);
    cardBody.appendChild(messageContent);
    cardBody.appendChild(voteContainer);

    return cardBody;
};


function votesBuilder(data) {
    const voteWrapper = document.createElement('div');
    voteWrapper.className = 'd-flex flex-row justify-content-left';

    const likeWrapper = document.createElement('div');
    likeWrapper.className = 'd-flex align-items-start';
    likeWrapper.style.padding = '.9rem 0rem 0rem 0rem';

    const likeForm = createVoteForm('like', data);
    likeWrapper.appendChild(likeForm);

    const dislikeWrapper = document.createElement('div');
    dislikeWrapper.className = 'd-flex align-items-start';
    dislikeWrapper.style.padding = '.9rem 0rem 0rem 0rem';

    const dislikeForm = createVoteForm('dislike', data);
    dislikeWrapper.appendChild(dislikeForm);

    voteWrapper.appendChild(likeWrapper);
    voteWrapper.appendChild(dislikeWrapper);

    return voteWrapper;
}


function createVoteForm(type, data) {
    const form = document.createElement('form');
    form.className = 'vote-form';
    form.dataset.messageId = data['message']['id'];

    const csrfTokenInput = document.createElement('input');
    csrfTokenInput.type = 'hidden';
    csrfTokenInput.name = 'csrfmiddlewaretoken';
    csrfTokenInput.value = csrftoken;

    const button = document.createElement('button');
    button.type = 'submit';
    button.className = 'btn';
    button.dataset.type = 'answer';
    button.dataset.action = type;

    const icon = document.createElement('i');
    icon.className = type === 'like' ? 'fa fa-thumbs-up fa-lg' : 'fa fa-thumbs-down fa-lg';
    icon.setAttribute('aria-hidden', 'true');

    const counterSpan = document.createElement('span');
    counterSpan.className = type === 'like' ? 'like-counter' : 'dislike-counter';
    counterSpan.id = `total-${type}s${data['message']['id']}`;
    counterSpan.textContent = '0';

    icon.appendChild(counterSpan);
    button.appendChild(icon);

    form.appendChild(csrfTokenInput);
    form.appendChild(button);

    return form;
}


document.querySelector('#send-answer').onclick = function (e) {
    e.preventDefault();
    const answerForm = document.querySelector('#content');
    const text = answerForm.value;
    answersSocket.send(JSON.stringify(
        {
            'text': text
        }
    ));
    answerForm.value = '';
};


answersSocket.onclose = function(e) {
    console.error('Answers socket closed unexpectedly');
};
