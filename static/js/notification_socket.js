const notificationList = document.getElementById('notification-list');
const pushNotificationList = document.getElementById('push-notification-list');
const notificationCounter = document.getElementById('notification-counter');
const username = JSON.parse(document.getElementById('username').textContent);
let notificationSocket;


if (username !== '') {
    notificationSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/notifications/'
        + username
        + '/'
    );

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data['type'] == 'send_notification') {
            if (notificationList !== null) {
                createNotification(data['notification']);
            };
            if (pushNotificationList !== null) {
                createPushNotification(data['notification']);
            };
            notificationCounter.innerHTML = parseInt(notificationCounter.textContent) + 1;

        } else if (data['type'] == 'show_unread_push_notifications') {
            showUnreadPushNotifications(data['notifications']);
            notificationCounter.innerHTML = data['count_notifications'];

        } else if (data['type'] == 'read_all_notifications') {
            pushNotificationList.innerHTML = '';
            notificationCounter.innerHTML = '0';

        };
    };

    notificationSocket.onopen = function(e) {
        notificationSocket.send(JSON.stringify(
            {
                'type': 'show_unread_push_notifications'
            }
        ));
    };

    notificationSocket.onclose = function(e) {
        console.error('Notification socket closed unexpectedly');
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

};


function createNotification(data) {
    var cardDiv = document.createElement('div');
    cardDiv.className = 'card text-dark bg-light mb-3 mt-3';

    var flexRowDiv = document.createElement('div');
    flexRowDiv.className = 'd-flex flex-row g-0';

    var flexColumnDiv = document.createElement('div');
    flexColumnDiv.className = 'd-flex flex-column';

    var link = document.createElement('a');
    link.href = data['url'];

    var messageDiv = document.createElement('div');
    messageDiv.className = 'p-3';

    var messageHeading = document.createElement('h5');
    messageHeading.id = 'notification-message';
    messageHeading.className = 'card-title';
    messageHeading.textContent = data['message'];

    messageDiv.appendChild(messageHeading);
    link.appendChild(messageDiv);

    var dateDiv = document.createElement('div');
    dateDiv.className = 'p-3 d-flex';

    var dateParagraph = document.createElement('p');
    dateParagraph.className = 'card-text';
    dateParagraph.textContent = data['created_at'];

    dateDiv.appendChild(dateParagraph);

    flexColumnDiv.appendChild(link);
    flexColumnDiv.appendChild(dateDiv);

    flexRowDiv.appendChild(flexColumnDiv);
    cardDiv.appendChild(flexRowDiv);

    notificationList.insertAdjacentElement('afterbegin', cardDiv);
};


function createPushNotification(data) {
    var listItem = document.createElement('li');

    var link = document.createElement('a');
    link.className = 'dropdown-item';
    link.href = data['url'];

    var columnDiv = document.createElement('div');
    columnDiv.className = 'd-flex flex-column';

    var messageSmall = document.createElement('small');
    messageSmall.className = 'text-muted';
    messageSmall.textContent = data['message'];

    var dateSmall = document.createElement('small');
    dateSmall.className = 'text-muted';
    dateSmall.textContent = data['created_at'];

    columnDiv.appendChild(messageSmall);
    columnDiv.appendChild(dateSmall);

    link.appendChild(columnDiv);
    listItem.appendChild(link);

    pushNotificationList.insertAdjacentElement('afterbegin', listItem);
};
