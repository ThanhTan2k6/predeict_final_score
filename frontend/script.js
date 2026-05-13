const URL = window.location.origin;

document.getElementById('predictBtn').onclick = async () => {
    const val = document.getElementById('midterm').value;
    if (val === "") return alert("Nhập điểm đã!");

    try {
        const res = await fetch(`${URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ midterm: val })
        });
        const data = await res.json();
        
        document.getElementById('score').innerText = data.final;
        document.getElementById('formula').innerText = `Model: y = ${data.w}x + ${data.b}`;
        document.getElementById('res').style.display = 'block';
    } catch (e) {
        alert("Lỗi kết nối server!");
    }
};