const questionId = JSON.parse(document.getElementById('questionId').textContent);
const answersSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/questions/' + questionId + '/'
);

answersSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    answersList = document.getElementById('answers-list');
    answersList.insertAdjacentHTML(
    'afterbegin',
    '<div class="card-body border rounded">' +
        '<div class="d-flex flex-start align-items-center">' +
            '<img class="rounded-circle shadow-1-strong me-3" src="'+ data['message']['profile_image'] +'" alt="avatar" width="60" height="60">'+
            '<div>' +
                '<h6 class="fw-bold text-primary mb-1">' +
                    '<a href="' + data['message']['author_url'] + '">' +
                        data['message']['author'] + 
                    "</a>" +
                '</h6>' +
                '<p class="text-muted small mb-0"> Опубликовано - ' + data['message']['date_published'] + '</p>' +
            '</div>' + 
        '</div>' +
        '<p class="mt-3 mb-4 pb-2">' + data['message']['content'] + '</p>' +
    '</div>'
    );
};

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