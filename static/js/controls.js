// JavaScript Document

function pushToPage(url) {
	new Image().src = url;
}

function setVolume(newValue) {
	pushToPage("/set-volume/" + newValue);
}

muteFlag = false;

function setMuteFlag(flag) {
	var imgElement = document.getElementById("mute");
	if (flag) {
		imgElement.src = "/static/icons/volume-mute.png";
	} else {
		imgElement.src = "/static/icons/volume-on.png";
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
	var selectElement = document.getElementById("state");
	return selectElement.options[index].text;
}

function setUpSelectedMode() {
	var index = document.getElementById("state").selectedIndex;
	var modeName = getModeString(index);
	var modeId = modeName.replace(/\s/g, "");
	var controlAreaElements = document.getElementsByClassName("ControlArea");
	for (var eIndex = 0; eIndex < controlAreaElements.length; eIndex++) {
		var element = controlAreaElements[eIndex];
		if (element.id == modeId) {
			element.style.display = "";
		} else {
			element.style.display = "none";
		}
	}
}

function setUpModeByIndex(index) {
	document.getElementById("state").selectedIndex = index;
	setUpSelectedMode()
}

function sendMode() {
	var index = document.getElementById("state").selectedIndex;
	pushToPage("/set-mode/" + getModeString(index));
	setUpSelectedMode();
}