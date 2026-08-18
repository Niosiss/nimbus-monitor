const loginButton = document.getElementById('login-button');
localStorage.removeItem('token');

loginButton.addEventListener('click', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const params = new URLSearchParams({ username: username, password: password });

    const response = await fetch('https://orange-sniffle-pjr75wq5pqg437q94-8000.app.github.dev/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params
    });
    
    if (response.ok) {
        const data = await response.json()
        localStorage.setItem('token', data.access_token)
        window.location.href = "index.html";
    } else {
        alert("Hatalı Kullanıcı Adı Veya Şifre.")
    }
});