// generate buttons
function make_buttons(oc) {
    oc.forEach(o => {
	    let btn = document.createElement('button');
    	btn.innerText = o;
	    btn.onclick=send_outcome;
    	btn_grid.appendChild(btn);
    });
}
fetch("/cats").then(r=>{
    r.json().then(j=>{
        make_buttons(j);
    })
})


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
