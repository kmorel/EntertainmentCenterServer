// JavaScript Document

function pushToPage(url) {
	new Image().src = url;
}

function setVolume(newValue) {
	pushToPage("/set-volume/" + newValue);
}

function setMute(newValue) {
	imgTag = find("mute");
	if (newValue == "on") {
		imgTag.src = "/static/icons/volume-mute.png";
		imgTag.onclick = "setMute('off')";
	} else {
		imgTag.src = "/static/icons/volume-on.png";
		imgTag.onclick = "setMute('on')";
	}
	pushToPage("/set-mute/" + newValue);
}
