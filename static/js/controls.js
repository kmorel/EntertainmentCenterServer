// JavaScript Document

function pushToPage(url) {
	new Image().src = url;
}

function setVolume(newValue) {
	pushToPage("/set-volume/" + newValue);
}

muteFlag = false;

function setMuteFlag(flag) {
	imgTag = document.getElementById("mute");
	if (flag) {
		imgTag.src = "/static/icons/volume-mute.png";
	} else {
		imgTag.src = "/static/icons/volume-on.png";
	}
	muteFlag = flag;
}

function sendMuteFlag(flag) {
	setMuteFlag(flag)
	pushToPage("/set-mute/" + (flag ? 1 : 0));
}

function toggleMute() {
	sendMuteFlag(!muteFlag)
}

function getModeString(index) {
	selectTag = document.getElementById("state");
	return selectTag.options[index].text;
}

function setUpMode(index) {
	pushToPage("/log/" + getModeString(index));
}
