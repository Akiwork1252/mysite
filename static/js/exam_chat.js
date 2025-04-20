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
        const userStrong = document.createElement('strong');
        userStrong.textContent = 'Answer: ';
        userDiv.appendChild(userStrong);
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
            // 採点結果表示
            const resultContainerDiv = document.createElement('div');

            const scoreDiv = document.createElement('div');
            scoreDiv.textContent = `Score: ${data.score}`;

            const explanationDiv = document.createElement('div');
            explanationDiv.textContent = `Explanation: ${data.explanation}`;

            resultContainerDiv.appendChild(scoreDiv);
            resultContainerDiv.appendChild(explanationDiv);
            chatBox.appendChild(resultContainerDiv)

            if (data.next_question) {
                // 次の問題
                const questionDiv = document.createElement('div');
                const questionStrong = document.createElement('strong');
                questionStrong.textContent = 'Question: ';
                questionDiv.appendChild(questionStrong);
                questionDiv.append(`${data.next_question}`);
                chatBox.appendChild(questionDiv);
            } else if (data.finished) {
                // 総スコア、メッセージ表示
                const totalScoreDiv = document.createElement('div');
                const messageDiv = document.createElement('div');
                const scoreStrong = document.createElement('strong');
                const aiStrong = document.createElement('strong')
                scoreStrong.textContent = 'TotalScore: ';
                aiStrong.textContent = 'AI: ';
                totalScoreDiv.appendChild(scoreStrong);
                totalScoreDiv.append(`${data.total_score}`);
                chatBox.appendChild(totalScoreDiv);
                messageDiv.appendChild(aiStrong);
                messageDiv.append(`${data.message}`);
                chatBox.appendChild(messageDiv);
            } else if (data.error) {
                console.error(data.error);
            }

            messageInput.value = '';
        });
    });
});