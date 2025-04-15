document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const endLectureButton = document.getElementById('end-lecture');
    const chatUrl = chatForm.dataset.url;
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // チャット送信
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userMessage = messageInput.value;

        // ユーザーのメッセージを表示
        const userDiv = document.createElement('div');
        userDiv.textContent = `User: ${userMessage}`;
        userDiv.classList.add('text-end', 'mb-2');
        chatBox.appendChild(userDiv);

        // サーバーにメッセージを送信
        fetch(chatUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const lines = data.lecture_response.split('\n');
            const aiDiv = document.createElement('div');
            aiDiv.classList.add('text-start', 'mb-2');

            lines.forEach(line => {
                const lineDiv = document.createElement('div');
                lineDiv.textContent = line;
                aiDiv.appendChild(lineDiv);
            });
            chatBox.appendChild(aiDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            messageInput.value = '';
        });
    });

    // 講義終了
    endLectureButton.addEventListener('click', function () {
        fetch(chatUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({ message: '終了' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        });
    });
});