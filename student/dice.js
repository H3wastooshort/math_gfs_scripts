possible_outcomes = [1,2,3,4,5,6]

// generate buttons
possible_outcomes.forEach(o => {
	let btn = document.createElement('button');
	btn.innerText = o;
	btn.onclick=send_outcome;
	btn_grid.appendChild(btn);
});

function send_outcome(evt) {
	evt.srcElement.style.borderColor = "orange";
	fetch("/outcome", {
		method: "POST",
		headers: {"Content-Type": "text/plain"},
		body: evt.srcElement.innerText
	})
	.then(r => {
		evt.srcElement.style.borderColor = r.ok ? "green" : "magenta";
	})
	.catch(err => {evt.srcElement.style.borderColor = "magenta";});
}
