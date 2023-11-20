const notificationList = document.getElementById('notification-list');
const pushNotificationList = document.getElementById('push-notification-list');
const notificationCounter = document.getElementById('notification-counter');
const username = JSON.parse(document.getElementById('username').textContent);
const notificationSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/notifications/'
    + username
    + '/'
);

notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data['type'] == 'send_notification') {
        if (notificationList !== null){
            createNotification(data['notification'])
        }
        createPushNotification(data['notification'])
        notificationCounter.innerHTML = parseInt(notificationCounter.textContent) + 1
    } else if (data['type'] == 'show_unread_push_notifications') {
        showUnreadPushNotifications(data['notifications'])
        notificationCounter.innerHTML = data['count_notifications']
    } else if (data['type'] == 'read_all_notifications') {
        pushNotificationList.innerHTML = '';
        notificationCounter.innerHTML = '0'
    }
};

notificationSocket.onopen = function(e) {
    notificationSocket.send(JSON.stringify(
        {
            'type': 'show_unread_push_notifications'
        }
    ));
};

function createNotification(data) {
    notificationList.insertAdjacentHTML(
        'afterbegin',
        '<div class="card text-dark bg-light mb-3 mt-3">' +
            '<div class="d-flex flex-row g-0">' +
                '<div class="d-flex flex-column">' +
                    '<a href=' + data['url'] + '>' +
                        '<div class="p-3">' +
                            '<h5 id="notification-message" class="card-title">' + data['message'] + '</h5>' +
                        '</div>' +
                    '</a>' +
                    '<div class="p-3 d-flex">' +
                        '<p class="card-text">' + data['created_at'] + '</p>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>'
    );
}

function createPushNotification(data) {
    pushNotificationList.insertAdjacentHTML(
        'afterbegin',
        '<li>' +
            '<a class="dropdown-item" href=' + data['url'] + '>' +
                '<p class="d-flex flex-column">' + 
                    '<small class="text-muted">' +
                        data['message'] +
                    '</small>' + 
                    '<small class="text-muted">' +
                        data['created_at'] +
                    '</small>' + 
                '</p>' +
            '</a>' +
        '</li>'
    );
};

function showUnreadPushNotifications(data) {
    for (const notification of data) {
        createPushNotification(notification);
    };
};

document.getElementById("read-all").onclick = function(e) {
    e.preventDefault();
    notificationSocket.send(JSON.stringify(
        {
            'type': 'read_all_notifications'
        }
    ))
};

notificationSocket.onclose = function(e) {
    console.error('Notification socket closed unexpectedly');
};
