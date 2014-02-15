// JavaScript Document

function getButtonSize() {
	var screenWidth = $(document).width();
	var screenHeight = $(document).height();

	// First guess, the display is 4 buttons across.
	var buttonSize = screenWidth/4;
	
	// Check to make sure the display is tall enough for this size. The height
	// must accomodate 4 buttons in the main area plus the power plus the mute
	// plus potentially tabs.
	if (screenHeight < buttonSize*7) {
		buttonSize = screenHeight/7;
	}

	return parseInt(buttonSize);
}

function initGUI() {
	var buttonSize = getButtonSize();
	var screenWidth = $(document).width();

	$('.PowerSelect').width(screenWidth - buttonSize - 50);

	$('#powerButton').width(buttonSize);
	$('#powerButton').height(buttonSize);

//	$('#mainArea').offset({ top:buttonSize, left:0 });
//	$('#mainArea').height(4*buttonSize);

//	$('#volumeArea').offset({ top:5*buttonSize, left:0 });
//	$('.VolumeSelect').position({ top:0, left:0 });
	$('.VolumeSelect').width(screenWidth - buttonSize - 40);

	$('#mute').width(buttonSize);
	$('#mute').height(buttonSize);
//	$('#mute').offset({ top:5*buttonSize, left:screenWidth - buttonSize - 5 });

	$('.ButtonPanel').width(4*buttonSize);
	$('.ButtonPanel').height(4*buttonSize);
}

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

function sendModeByIndex(index) {
	document.getElementById("state").selectedIndex = index;
	sendMode()
}

function sendTiVo(ircode) {
	pushToPage("/tivo/ircommand/" + ircode);
}

function sendTiVoBack(t) {
	pushToPage("/tivo/skip-back/" + t);
}

function sendTiVoForward(t) {
	pushToPage("/tivo/skip-forward/" + t);
}

function sendTiVoGoTo(screen) {
	pushToPage("/tivo/goto/" + screen);
}