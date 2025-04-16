document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const endExamButton = document.getElementById('end-exam');
    const chatUrl = chatForm.dataset.url;
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // チャット送信
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userAnswer = messageInput.value;

        // ユーザーの回答を表示
        const userDiv = document.createElement('div');
        const strong = document.createElement('strong');
        strong.textContent = 'Answer: ';
        userDiv.appendChild(strong);
        userDiv.append(`${userAnswer}`);
        chatBox.appendChild(userDiv);

        // サーバーに回答を送信
        fetch(chatUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: new URLSearchParams({ answer: userAnswer })
        })
        .then(response => response.json())
        .then(data => {
            if ()
        })
    })
})