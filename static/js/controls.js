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
	// Some padding to remove from widths to compensate for scroll bars,
	// which tend to be larger on larger displays.
	var widthFudge = 10;
	if (screenWidth > 700) {
		widthFudge = 40;
	}

	$('.PowerSelect').width(screenWidth - buttonSize - widthFudge - 10);

	$('#powerButton').width(buttonSize);
	$('#powerButton').height(buttonSize);

	$('.VolumeSelect').width(screenWidth - buttonSize - widthFudge);

	$('#mute').width(buttonSize);
	$('#mute').height(buttonSize);

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
		$('#mute').attr("src", "/static/icons/volume-mute.png");
	} else {
		$('#mute').attr("src", "/static/icons/volume-on.png");
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

function getModeString() {
	return $('#state').val();
}

function setUpSelectedMode() {
	var modeName = getModeString();
	var modeId = modeName.replace(/\s/g, "");
	$('.ControlArea').each(function(index) {
		if (this.id == modeId) {
			this.style.display = '';
		} else {
			this.style.display = 'none';
		}
	});
}

function setUpModeByName(modeName) {
	$('#state').val(modeName).attr('selected', true).siblings('option').removeAttr('selected');
	$('#state').selectmenu('refresh', true);
	setUpSelectedMode();
}

function sendMode() {
	pushToPage("/set-mode/" + getModeString());
	setUpSelectedMode();
}

function sendModeByName(modeName) {
	setUpModeByName(modeName);
	sendMode();
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
