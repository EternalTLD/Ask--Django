$( document ).ready(function() {
    const pk = JSON.parse(document.getElementById('obj_id').textContent);
    const likeForm = $(`#vote-like-form${pk}`);
    const dislikeForm = $(`#vote-dislike-form${pk}`);
    const likeCounter = document.getElementById(`total-likes${pk}`);
    const dislikeCounter = document.getElementById(`total-dislikes${pk}`);
    const domain = window.location.origin;

    likeForm.on("submit", function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();

        var likeBtn = $(this).find('button');
        var type = likeBtn.data('type');

        $.ajax({
            type: 'POST',
            url: domain + '/votes/' + type + '/like/' + pk + '/',
            data: {
                'pk': pk,
                'csrfmiddlewaretoken': csrftoken
            },

            success: function(response) {
                likeCounter.innerHTML = response.total_likes;
                dislikeCounter.innerHTML = response.total_dislikes;
            },

        });
    });

    dislikeForm.on("submit", function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();

        var dislikeBtn = $(this).find('button');
        var type = dislikeBtn.data('type');

        $.ajax({
            type: 'POST',
            url: domain + '/votes/' + type + '/dislike/' + pk + '/',
            data: {
                'pk': pk,
                'csrfmiddlewaretoken': csrftoken
            },

            success: function(response) {
                likeCounter.innerHTML = response.total_likes;
                dislikeCounter.innerHTML = response.total_dislikes;
            },
            
        });
    });

});