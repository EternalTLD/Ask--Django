$(document).ready(function () {
    const domain = window.location.origin;

    function handleSubmission(pk, type, action, likeCounter, dislikeCounter) {
        $.ajax({
            type: 'POST',
            url: domain + '/votes/' + type + '/' + action + '/' + pk + '/',
            data: {
                'pk': pk,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function (response) {
                likeCounter.innerHTML = response.total_likes;
                dislikeCounter.innerHTML = response.total_dislikes;
            },
        });
    }

    $(document).on("submit", ".vote-form", function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        const form = $(this);
        const type = form.find('button').data('type');
        const action = form.find('button').data('action');
        const pk = form.data('message-id');
        const likeCounter = document.getElementById(`total-likes${pk}`);
        const dislikeCounter = document.getElementById(`total-dislikes${pk}`);
        handleSubmission(pk, type, action, likeCounter, dislikeCounter);
    });
});