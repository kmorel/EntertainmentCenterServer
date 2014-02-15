// JavaScript Document

function getButtonSize() {
	var screenWidth = $(document).width();
	var screenHeight = $(document).height();
	// Use the state height as representative of the size of elements such as tabs.
	var widgetHeight = $('#state').height();

	// First guess, the display is 4 buttons across.
	var buttonSize = screenWidth/4;
	
	// Check to make sure the display is tall enough for this size. The height
	// must accomodate 4 buttons in the main area plus the power plus the mute
	// plus potentially tabs.
	if (screenHeight < buttonSize*6 + widgetHeight) {
		buttonSize = (screenHeight - widgetHeight)/6;
	}
	
	// Make sure that the button size is at least as high as the standard mobile widgets.
	if (buttonSize < widgetHeight) {
		buttonSize = widgetHeight;
	}

	return parseInt(buttonSize);
}

function initGUI() {
	var buttonSize = getButtonSize();
	var screenWidth = $(document).width();

	$('.PowerSelect').offset({ top: 5, left:5 });
	$('.PowerSelect').width(screenWidth - buttonSize - 15);

	$('#powerButton').width(buttonSize);
	$('#powerButton').height(buttonSize);
	$('#powerButton').offset({ top:0, left:screenWidth - buttonSize - 5 });

	$('#mainArea').offset({ top:buttonSize, left:0 });

	$('#volumeArea').offset({ top:5*buttonSize, left:0 });
	$('.VolumeSelect').position({ top:0, left:0 });
	$('.VolumeSelect').width(screenWidth - buttonSize - 15);

	$('#mute').width(buttonSize);
	$('#mute').height(buttonSize);
	$('#mute').offset({ top:5*buttonSize, left:screenWidth - buttonSize - 5 });
}

function switchToNavigation() {
	var navigationAreaElements = document.getElementsByClassName("NavigationArea");
	for (var eIndex = 0; eIndex < navigationAreaElements.length; eIndex++) {
		var element = navigationAreaElements[eIndex];
		element.className = "NavigationArea";
	}
	var playbackAreaElements = document.getElementsByClassName("PlaybackArea");
	for (var eIndex = 0; eIndex < playbackAreaElements.length; eIndex++) {
		var element = playbackAreaElements[eIndex];
		element.className = "PlaybackArea HiddenPane";
	}
	var navigationTabElements = document.getElementsByClassName("NavigationTab");
	for (var eIndex = 0; eIndex < navigationTabElements.length; eIndex++) {
		var element = navigationTabElements[eIndex];
		element.className = "NavigationTab";
	}
	var playbackTabElements = document.getElementsByClassName("PlaybackTab");
	for (var eIndex = 0; eIndex < playbackTabElements.length; eIndex++) {
		var element = playbackTabElements[eIndex];
		element.className = "PlaybackTab InactiveTab";
	}
}

function switchToPlayback() {
	var navigationAreaElements = document.getElementsByClassName("NavigationArea");
	for (var eIndex = 0; eIndex < navigationAreaElements.length; eIndex++) {
		var element = navigationAreaElements[eIndex];
		element.className = "NavigationArea HiddenPane";
	}
	var playbackAreaElements = document.getElementsByClassName("PlaybackArea");
	for (var eIndex = 0; eIndex < playbackAreaElements.length; eIndex++) {
		var element = playbackAreaElements[eIndex];
		element.className = "PlaybackArea";
	}
	var navigationTabElements = document.getElementsByClassName("NavigationTab");
	for (var eIndex = 0; eIndex < navigationTabElements.length; eIndex++) {
		var element = navigationTabElements[eIndex];
		element.className = "NavigationTab InactiveTab";
	}
	var playbackTabElements = document.getElementsByClassName("PlaybackTab");
	for (var eIndex = 0; eIndex < playbackTabElements.length; eIndex++) {
		var element = playbackTabElements[eIndex];
		element.className = "PlaybackTab";
	}
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