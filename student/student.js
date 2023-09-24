possible_outcomes = [1,2,3,4,5,6]

// generate buttons
possible_outcomes.forEach(o => {
	let div = document.createElement('div');
	div.className="btn_cell";
	let btn = document.createElement('button');
	btn.innerText = o;
	btn.onclick=send_outcome;
	div.appendChild(btn);
	btn_grid.appendChild(div);
});

function send_outcome(evt) {
	evt.srcElement.style.borderColor = "cyan";
	fetch("/outcome", {
		method: "POST",
		headers: {"Content-Type": "text/plain"},
		body: evt.srcElement.innerText
	})
	.then(r => {
		evt.srcElement.style.borderColor = r.ok ? "white" : "red";
		if (!r.ok) r.text().then(t=>{alert("SERVER ERROR:\n" + t)});
	})
	.catch(err => {
		evt.srcElement.style.borderColor = "red";
		alert("CLIENT ERROR:\n"+err.message);
	});
}
